/**
 * Digital Dollar Wallet Manager
 * Biometric enrollment and management
 */
const { exec } = require('child_process');
const crypto = require('crypto');
const dd = require('../core/digital-dollar');

class WalletManager {
    // Enroll new user with biometric
    async enroll(userId, name) {
        return new Promise((resolve) => {
            // Termux fingerprint enrollment
            exec(`termux-fingerprint -t "Digital Dollar Enrollment" -d "Enroll ${name} in Digital Dollar"`,
                (err, stdout) => {
                    try {
                        const result = JSON.parse(stdout);
                        if (result.auth_result === 'AUTH_RESULT_SUCCESS') {
                            const bioHash = crypto.createHash('sha256')
                                .update(userId + Date.now() + 'DD_SALT')
                                .digest('hex');
                            const wallet = dd.createWallet(bioHash, userId);
                            // Mint welcome bonus
                            dd.mint(wallet.id, 10, 'Welcome bonus');
                            resolve({
                                success: true,
                                wallet_id: wallet.id,
                                welcome_bonus: 10,
                                message: `Welcome ${name}! Your Digital Dollar wallet is ready.`
                            });
                        } else {
                            resolve({ success: false, error: 'Biometric enrollment failed' });
                        }
                    } catch {
                        // Demo mode
                        const bioHash = crypto.createHash('sha256')
                            .update(userId + Date.now())
                            .digest('hex');
                        const wallet = dd.createWallet(bioHash, userId);
                        dd.mint(wallet.id, 10, 'Welcome bonus');
                        resolve({
                            success: true,
                            wallet_id: wallet.id,
                            welcome_bonus: 10,
                            demo: true
                        });
                    }
                }
            );
        });
    }

    // Authenticate and get wallet
    async authenticate(userId) {
        return new Promise((resolve) => {
            exec(`termux-fingerprint -t "Digital Dollar" -d "Authenticate payment"`,
                (err, stdout) => {
                    try {
                        const result = JSON.parse(stdout);
                        resolve({
                            authenticated: result.auth_result === 'AUTH_RESULT_SUCCESS',
                            userId,
                            timestamp: Date.now()
                        });
                    } catch {
                        resolve({ authenticated: false, error: 'Auth failed' });
                    }
                }
            );
        });
    }
}

module.exports = new WalletManager();
