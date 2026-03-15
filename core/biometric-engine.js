const { exec } = require('child_process');
const crypto = require('crypto');

class BiometricEngine {
    constructor() { this.sessionStore = new Map(); }

    async authenticateFingerprint(title) {
        return new Promise((resolve) => {
            exec(`termux-fingerprint -t "${title}"`, (err, stdout) => {
                try {
                    const r = JSON.parse(stdout);
                    resolve({ success: r.auth_result === 'AUTH_RESULT_SUCCESS', result: r.auth_result });
                } catch { resolve({ success: false, result: 'ERROR' }); }
            });
        });
    }

    createSession(userId) {
        const id = crypto.randomUUID();
        const session = { id, user_id: userId, created_at: Date.now(), expires_at: Date.now() + 86400000 };
        this.sessionStore.set(id, session);
        return session;
    }

    verifySession(sessionId) {
        const s = this.sessionStore.get(sessionId);
        if (!s) return { valid: false };
        if (Date.now() > s.expires_at) return { valid: false, reason: 'expired' };
        return { valid: true, session: s };
    }
}

module.exports = new BiometricEngine();
