// src/configs/env.config.ts
import dotenv from 'dotenv';
dotenv.config();

export const ENV_CONFIG = {
    TELEGRAM: {
        API_ID: process.env.TG_API_ID || '',
        API_HASH: process.env.TG_API_HASH || '',
        SESSION_NAME: process.env.TG_SESSION_NAME || 'haineo_session',
        SIGNAL_CHANNELS: (process.env.TG_CHANNELS || '').split(','),
    },
    MT5: {
        LOGIN: Number(process.env.MT5_LOGIN) || 0,
        PASSWORD: process.env.MT5_PASSWORD || '',
        SERVER: process.env.MT5_SERVER || '',
        PATH: process.env.MT5_PATH || 'C:\\Program Files\\MetaTrader 5\\terminal64.exe',
    },
    RISK: {
        DEFAULT_PERCENT: Number(process.env.RISK_PERCENT) || 1.0, // 1%
    }
};
