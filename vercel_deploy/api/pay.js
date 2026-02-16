const axios = require('axios');

module.exports = async (req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { order_id, amount, currency, preset_name, customer_email } = req.body;

    if (!order_id || amount === undefined || amount === null) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const parsedAmount = Number(amount);
    if (!Number.isFinite(parsedAmount) || parsedAmount <= 0) {
        return res.status(400).json({ error: 'Invalid amount. Amount must be a positive number.' });
    }

    const SERVER_KEY = process.env.MIDTRANS_SERVER_KEY || '';
    const MIDTRANS_IS_PRODUCTION_ENV = String(process.env.MIDTRANS_IS_PRODUCTION || '').toLowerCase();

    // 🛡️ GOD-MODE: Auto-detect environment based on key prefix
    // If key starts with 'Mid-server-', it's explicitly Production.
    // If it starts with 'SB-Mid-server-', it's Sandbox.
    let IS_PRODUCTION = ['1', 'true', 'yes', 'production'].includes(MIDTRANS_IS_PRODUCTION_ENV);

    if (SERVER_KEY.startsWith('Mid-server-')) {
        IS_PRODUCTION = true;
    } else if (SERVER_KEY.startsWith('SB-Mid-server-')) {
        IS_PRODUCTION = false;
    }

    const API_URL = IS_PRODUCTION
        ? 'https://app.midtrans.com/snap/v1/transactions'
        : 'https://app.sandbox.midtrans.com/snap/v1/transactions';

    console.log(`[Midtrans] Environment: ${IS_PRODUCTION ? 'PRODUCTION' : 'SANDBOX'} | Key Prefix: ${SERVER_KEY.substring(0, 10)}...`);

    if (!SERVER_KEY || SERVER_KEY.includes('XXXXX')) {
        return res.status(500).json({
            error: 'MIDTRANS_SERVER_KEY is not set or is still a placeholder. Please check Vercel Environment Variables.'
        });
    }

    if (IS_PRODUCTION && SERVER_KEY.startsWith('SB-')) {
        return res.status(500).json({
            error: 'CRITICAL Mismatch: MIDTRANS_IS_PRODUCTION is TRUE but SERVER_KEY is a Sandbox key (SB-).'
        });
    }

    const authHeader = Buffer.from(`${SERVER_KEY}:`).toString('base64');

    const payload = {
        transaction_details: {
            order_id: order_id,
            gross_amount: Math.round(parsedAmount)
        },
        item_details: [
            {
                id: 'subscription',
                price: Math.round(parsedAmount),
                quantity: 1,
                name: preset_name || 'Haineo AI Subscription'
            },
        ],
        customer_details: {
            first_name: 'Haineo Trader',
            email: customer_email || 'trader@haineo.ai'
        },
        callbacks: {
            finish: 'https://telegramcopytrade.vercel.app/payment/success',
            error: 'https://telegramcopytrade.vercel.app/payment/error',
            unfinish: 'https://telegramcopytrade.vercel.app/payment/unfinish'
        }
    };

    if (currency) {
        payload.transaction_details.currency = currency.toUpperCase();
    }

    try {
        const response = await axios.post(API_URL, payload, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Basic ${authHeader}`
            }
        });

        return res.status(200).json({
            ...response.data,
            snap_environment: IS_PRODUCTION ? 'production' : 'sandbox'
        });
    } catch (error) {
        console.error('Midtrans API Error:', error.response ? error.response.data : error.message);
        return res.status(error.response ? error.response.status : 500).json(
            error.response ? error.response.data : { error: 'Internal Server Error' }
        );
    }
};
