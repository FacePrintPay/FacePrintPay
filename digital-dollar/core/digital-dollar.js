/**
 * Digital Dollar - Sovereign Biometric Currency Engine
 * Author: Cygel White / FacePrintPay
 * "Your face is your wallet"
 */
const crypto = require('crypto');
const { exec } = require('child_process');

class DigitalDollar {
    constructor() {
        this.ledger = new Map();
        this.txHistory = [];
        this.totalSupply = 0;
        this.symbol = 'DD$';
        this.name = 'Digital Dollar';
    }

    // Create biometric wallet - no keys, just your face
    createWallet(biometricHash, userId) {
        const walletId = 'DD_' + crypto.createHash('sha256')
            .update(biometricHash + userId)
            .digest('hex').substring(0, 16).toUpperCase();

        const wallet = {
            id: walletId,
            user_id: userId,
            biometric_hash: biometricHash,
            balance: 0,
            created_at: Date.now(),
            tx_count: 0,
            status: 'active'
        };

        this.ledger.set(walletId, wallet);
        console.log(`✅ Wallet created: ${walletId}`);
        return wallet;
    }

    // Get wallet by biometric - your face unlocks it
    getWalletByBiometric(biometricHash, userId) {
        const walletId = 'DD_' + crypto.createHash('sha256')
            .update(biometricHash + userId)
            .digest('hex').substring(0, 16).toUpperCase();
        return this.ledger.get(walletId) || null;
    }

    // Mint Digital Dollars (admin/system only)
    mint(walletId, amount, reason) {
        const wallet = this.ledger.get(walletId);
        if (!wallet) throw new Error('Wallet not found');

        wallet.balance += amount;
        this.totalSupply += amount;

        const tx = this.recordTx({
            type: 'MINT',
            to: walletId,
            amount,
            reason,
            balance_after: wallet.balance
        });

        console.log(`💵 Minted ${amount} DD$ to ${walletId}`);
        return { wallet, tx };
    }

    // Send Digital Dollars - biometric verified
    async send({ fromWallet, toWallet, amount, biometricVerified, memo }) {
        if (!biometricVerified) throw new Error('Biometric verification required');

        const sender = this.ledger.get(fromWallet);
        const receiver = this.ledger.get(toWallet);

        if (!sender) throw new Error('Sender wallet not found');
        if (!receiver) throw new Error('Receiver wallet not found');
        if (sender.balance < amount) throw new Error('Insufficient balance');

        sender.balance -= amount;
        receiver.balance += amount;
        sender.tx_count++;
        receiver.tx_count++;

        const tx = this.recordTx({
            type: 'TRANSFER',
            from: fromWallet,
            to: toWallet,
            amount,
            memo: memo || '',
            sender_balance_after: sender.balance,
            receiver_balance_after: receiver.balance
        });

        console.log(`✅ Sent ${amount} DD$ from ${fromWallet} to ${toWallet}`);
        return { tx, sender, receiver };
    }

    // Pay at merchant - biometric checkout
    async pay({ buyerBiometric, buyerId, merchantId, amount, memo }) {
        const buyer = this.getWalletByBiometric(buyerBiometric, buyerId);
        if (!buyer) throw new Error('Buyer wallet not found - enroll first');
        if (buyer.balance < amount) throw new Error(`Insufficient DD$ balance: ${buyer.balance}`);

        const merchant = this.ledger.get(merchantId);
        if (!merchant) throw new Error('Merchant not found');

        buyer.balance -= amount;
        merchant.balance += amount;

        const tx = this.recordTx({
            type: 'PAYMENT',
            from: buyer.id,
            to: merchantId,
            amount,
            memo: memo || 'Digital Dollar Payment',
            method: 'BIOMETRIC',
            buyer_balance_after: buyer.balance
        });

        return { success: true, tx, buyer_balance: buyer.balance };
    }

    // Record transaction with hash
    recordTx(data) {
        const tx = {
            id: 'TX_' + Date.now() + '_' + Math.random().toString(36).substr(2,6).toUpperCase(),
            timestamp: Date.now(),
            hash: crypto.createHash('sha256')
                .update(JSON.stringify(data) + Date.now())
                .digest('hex'),
            ...data
        };
        this.txHistory.push(tx);
        return tx;
    }

    getBalance(walletId) {
        const w = this.ledger.get(walletId);
        return w ? w.balance : 0;
    }

    getLedgerStats() {
        return {
            total_wallets: this.ledger.size,
            total_supply: this.totalSupply,
            total_transactions: this.txHistory.length,
            symbol: this.symbol,
            name: this.name
        };
    }
}

module.exports = new DigitalDollar();
