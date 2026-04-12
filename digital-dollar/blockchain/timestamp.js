/**
 * Digital Dollar - Bitcoin OTS Timestamping
 * Every transaction anchored to Bitcoin blockchain
 */
const { exec } = require('child_process');
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

class BitcoinTimestamp {
    constructor() {
        this.otsDir = process.env.HOME + '/.digital-dollar/ots';
        try { fs.mkdirSync(this.otsDir, { recursive: true }); } catch {}
    }

    // Stamp a transaction to Bitcoin
    async stampTransaction(tx) {
        const txData = JSON.stringify(tx);
        const hash = crypto.createHash('sha256').update(txData).digest('hex');
        const txFile = path.join(this.otsDir, `${tx.id}.json`);

        fs.writeFileSync(txFile, txData);

        return new Promise((resolve) => {
            exec(`ots stamp ${txFile} 2>/dev/null`, (err, stdout) => {
                if (!err) {
                    resolve({
                        stamped: true,
                        tx_id: tx.id,
                        hash,
                        ots_file: txFile + '.ots',
                        message: 'Transaction anchored to Bitcoin blockchain'
                    });
                } else {
                    // OTS not installed - record hash only
                    resolve({
                        stamped: false,
                        tx_id: tx.id,
                        hash,
                        message: 'Hash recorded - install ots for Bitcoin anchoring'
                    });
                }
            });
        });
    }

    // Verify transaction on Bitcoin
    async verifyTransaction(txId) {
        const otsFile = path.join(this.otsDir, `${txId}.json.ots`);
        return new Promise((resolve) => {
            exec(`ots verify ${otsFile} 2>/dev/null`, (err, stdout) => {
                resolve({
                    verified: !err,
                    tx_id: txId,
                    output: stdout || 'OTS not available'
                });
            });
        });
    }
}

module.exports = new BitcoinTimestamp();
