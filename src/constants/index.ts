// src/constants/index.ts

export const TRADING_CONSTANTS = {
  MAGIC_NUMBER: 123456,
  DEFAULT_DEVIATION: 10,
  COMMENT_PREFIX: "Haineo Auto-Trade",
};

export const SIGNAL_REGEX = {
  SYMBOL: /\b([A-Z]{3,}|XAUUSD|GOLD|US30|NAS100)\b/i,
  ACTION: /\b(BUY|SELL|LONG|SHORT|LIMIT|STOP)\b/i,
  PRICE: /\b\d+(?:\.\d+)?\b/g,
};
