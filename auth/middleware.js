const engine = require('../core/biometric-engine');

const requireBiometric = (req, res, next) => {
    const sid = req.headers['x-mybuyo-session'];
    if (!sid) return res.status(401).json({ error: 'biometric_required' });
    const { valid, session, reason } = engine.verifySession(sid);
    if (!valid) return res.status(401).json({ error: 'invalid', reason });
    req.biometricSession = session;
    next();
};

const requirePaymentAuth = (req, res, next) => {
    const sid = req.headers['x-mybuyo-session'];
    const { valid, session } = engine.verifySession(sid);
    if (!valid) return res.status(401).json({ error: 'auth_required' });
    if (Date.now() - session.created_at > 300000) return res.status(401).json({ error: 'stale_session' });
    req.biometricSession = session;
    next();
};

module.exports = { requireBiometric, requirePaymentAuth };
