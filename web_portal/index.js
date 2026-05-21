require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY || 'sk_test_placeholder');
const si = require('systeminformation');
const path = require('path');

const app = express();
app.use(helmet());
app.use(express.json());
app.use(express.static('public'));

// API Key Management Simulation
const apiKeys = new Map();

app.post('/api/generate-key', (req, res) => {
    const newKey = `nexus_${require('crypto').randomBytes(16).toString('hex')}`;
    // Simplified for demonstration - needs proper user context in production
    apiKeys.set('default_user', newKey);
    res.json({ apiKey: newKey });
});

// Subscription Placeholder
app.post('/api/subscribe', async (req, res) => {
    res.json({ message: "Subscription portal active." });
});

// System Status Dashboard Endpoint
app.get('/api/system-status', async (req, res) => {
    try {
        const cpu = await si.cpu();
        const mem = await si.mem();
        res.json({ cpu, mem });
    } catch (e) {
        res.status(500).send(e.toString());
    }
});

app.listen(3000, () => console.log('Secure portal online on port 3000.'));
