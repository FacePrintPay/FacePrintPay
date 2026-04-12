const express = require('express');
const app = express();
const PORT = 3003;

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'swarm_api' });
});

app.get('/', (req, res) => {
    res.json({ 
        service: 'Swarm API',
        version: '1.0.0',
        status: 'operational'
    });
});

app.listen(PORT, () => {
    console.log(`Swarm API running on port ${PORT}`);
});
