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
app.use(express.static(path.join(__dirname, 'public')));

const apiKeys = new Map();

app.post('/api/generate-key', (req, res) => {
    const newKey = `sentinel_${require('crypto').randomBytes(16).toString('hex')}`;
    // Enterprise user context management
    apiKeys.set('default_user', newKey);
    res.json({ apiKey: newKey });
});

const { GoogleGenerativeAI } = require("@google/generative-ai");

// Gemini Integration
let genAI;
if (process.env.GEMINI_API_KEY) {
    genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
}

// ... existing routes ...

app.post('/api/chat', async (req, res) => {
    const { directive } = req.body;
    const apiKey = req.headers['x-api-key'];
    if (!apiKey) return res.status(401).json({ error: "Gemini API key header missing." });
    
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    
    try {
        const userGenAI = new GoogleGenerativeAI(apiKey);
        const model = userGenAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContentStream(directive);
        
        for await (const chunk of result.stream) {
            const chunkText = chunk.text();
            res.write(`data: ${JSON.stringify({ response: chunkText })}\n\n`);
        }
        res.end();
    } catch (e) {
        res.write(`data: ${JSON.stringify({ error: e.message })}\n\n`);
        res.end();
    }
});

// Enterprise Security Telemetry Endpoint
app.get('/api/security-telemetry', (req, res) => {
    const filePath = path.join(__dirname, '../data/sec_ops_telemetry.json');
    if (require('fs').existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        res.status(404).json({ error: "Telemetry data not found" });
    }
});

app.listen(3001, () => console.log('Secure portal online on port 3001.'));
