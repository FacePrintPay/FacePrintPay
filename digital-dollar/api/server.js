/**
 * Digital Dollar API Server
 * Author: Cygel White / FacePrintPay
 */
const express = require('express');
const cors = require('cors');
const dd = require('../core/digital-dollar');
const walletMgr = require('../wallet/wallet-manager');
const btc = require('../blockchain/timestamp');

const app = express();
app.use(express.json());
app.use(cors());

// Health
app.get('/', (req, res) => res.json({
    service: 'Digital Dollar API',
    version: '1.0.0',
    symbol: 'DD$',
    tagline: 'Your face is your wallet',
    author: 'Cygel White / FacePrintPay',
    status: 'online',
    stats: dd.getLedgerStats()
}));

// Enroll new wallet
app.post('/wallet/enroll', async (req, res) => {
    try {
        const { user_id, name } = req.body;
        if (!user_id || !name) return res.status(400).json({ error: 'user_id and name required' });
        const result = await walletMgr.enroll(user_id, name);
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get balance
app.get('/wallet/:walletId/balance', (req, res) => {
    const balance = dd.getBalance(req.params.walletId);
    res.json({ wallet_id: req.params.walletId, balance, symbol: 'DD$' });
});

// Send DD$
app.post('/wallet/send', async (req, res) => {
    try {
        const { from, to, amount, biometric_session, memo } = req.body;

        // Verify session from MyBuyo
        const biometricVerified = !!biometric_session;

        const result = await dd.send({
            fromWallet: from,
            toWallet: to,
            amount: parseFloat(amount),
            biometricVerified,
            memo
        });

        // Stamp to Bitcoin
        btc.stampTransaction(result.tx);

        res.json({ success: true, ...result });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// Pay at merchant (biometric checkout)
app.post('/pay', async (req, res) => {
    try {
        const { user_id, merchant_id, amount, memo } = req.body;

        // Get biometric auth from MyBuyo
        const auth = await walletMgr.authenticate(user_id);
        if (!auth.authenticated) {
            return res.status(401).json({ error: 'Biometric authentication failed' });
        }

        const bioHash = require('crypto').createHash('sha256')
            .update(user_id + Date.now() + 'DD_SALT')
            .digest('hex');

        const result = await dd.pay({
            buyerBiometric: bioHash,
            buyerId: user_id,
            merchantId: merchant_id,
            amount: parseFloat(amount),
            memo
        });

        btc.stampTransaction(result.tx);
        res.json(result);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// Ledger stats
app.get('/ledger', (req, res) => {
    res.json(dd.getLedgerStats());
});

// Transaction history
app.get('/transactions', (req, res) => {
    res.json({
        count: dd.txHistory.length,
        transactions: dd.txHistory.slice(-20)
    });
});

// Mint (admin)
app.post('/admin/mint', (req, res) => {
    try {
        const { wallet_id, amount, reason } = req.body;
        const result = dd.mint(wallet_id, parseFloat(amount), reason);
        res.json({ success: true, ...result });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 3005;
app.listen(PORT, () => {
    console.log('💵 Digital Dollar API - ONLINE');
    console.log(`   Port:    ${PORT}`);
    console.log(`   Symbol:  DD$`);
    console.log(`   Enroll:  POST /wallet/enroll`);
    console.log(`   Pay:     POST /pay`);
    console.log(`   Balance: GET  /wallet/:id/balance`);
    console.log(`   Author:  Cygel White / FacePrintPay`);
});
