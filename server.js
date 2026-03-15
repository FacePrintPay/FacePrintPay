const express = require('express');
const engine = require('./core/biometric-engine');
const { requireBiometric, requirePaymentAuth } = require('./auth/middleware');
const pay = require('./packages/pay');

const app = express();
app.use(express.json());

app.get('/', (req, res) => res.json({
    service: 'MyBuyo Biometric SaaS',
    version: '1.0.0',
    author: 'Cygel White / FacePrintPay',
    status: 'online',
    ports: { auth: 3004, pay: 3004 }
}));

app.post('/auth/fingerprint', async (req, res) => {
    const result = await engine.authenticateFingerprint('MyBuyo');
    if (result.success) {
        const session = engine.createSession(req.body.user_id || 'user_' + Date.now());
        res.json({ success: true, session_id: session.id });
    } else {
        res.status(401).json({ success: false });
    }
});

app.get('/auth/verify', requireBiometric, (req, res) => {
    res.json({ valid: true, session: req.biometricSession });
});

app.post('/pay', requirePaymentAuth, async (req, res) => {
    const result = await pay.verifyAndPay({
        from: req.biometricSession.user_id,
        to: req.body.to,
        amount: req.body.amount,
        sessionId: req.headers['x-mybuyo-session']
    });
    res.json(result);
});

app.listen(3004, () => console.log('🔐 MyBuyo on 3004'));
