const engine = require('../core/biometric-engine');
const crypto = require('crypto');

class MyBuyoPay {
    async verifyAndPay({ from, to, amount, sessionId }) {
        const { valid } = engine.verifySession(sessionId);
        if (!valid) throw new Error('Auth required');
        return {
            success: true,
            tx_hash: crypto.createHash('sha256').update(`${from}${to}${amount}${Date.now()}`).digest('hex'),
            from, to, amount,
            biometric_verified: true,
            timestamp: Date.now()
        };
    }
}

module.exports = new MyBuyoPay();
