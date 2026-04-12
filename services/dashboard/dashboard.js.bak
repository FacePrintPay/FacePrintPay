const express = require('express');
const app = express();
const PORT = 3001;

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'dashboard' });
});

app.get('/', (req, res) => {
    res.json({ 
        service: 'Dashboard',
        version: '1.0.0',
        status: 'operational'
    });
});

app.listen(PORT, () => {
    console.log(`Dashboard service running on port ${PORT}`);
});
