const express = require('express');
const path = require('path');
const app = express();
const port = 3001;

// Serve static files from the current directory
app.use(express.static('.'));

// Ensure root serves index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
    console.log(`Dashboard UI running on http://localhost:${port}`);
});
