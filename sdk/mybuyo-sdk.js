class MyBuyoSDK {
    constructor(config = {}) {
        this.baseUrl = config.baseUrl || 'http://localhost:3004';
        this.session = null;
    }
    async authenticate() {
        const res = await fetch(`${this.baseUrl}/auth/fingerprint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const data = await res.json();
        if (data.session_id) this.session = data.session_id;
        return data;
    }
    async pay({ to, amount }) {
        return fetch(`${this.baseUrl}/pay`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-mybuyo-session': this.session },
            body: JSON.stringify({ to, amount })
        }).then(r => r.json());
    }
    isAuthenticated() { return !!this.session; }
}
if (typeof module !== 'undefined') module.exports = MyBuyoSDK;
