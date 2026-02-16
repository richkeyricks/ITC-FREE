// src/index.ts
import { SignalParserService } from './modules/parser/signal-parser.service';
import { MT5ExecutorService } from './modules/mt5/mt5-executor.service';

// --- INITIALIZATION ---
const parser = new SignalParserService();
const executor = new MT5ExecutorService();

async function main() {
    console.log("Haineo Telegram-to-MT5 Bridge Started.");

    // Example Message from Telegram
    const exampleMessage = "GOLD BUY NOW @ 2025.50 SL 2010 TP 2045";

    console.log(`// Received Message: ${exampleMessage}`);

    const signal = parser.parse(exampleMessage);

    if (signal) {
        console.log("// Signal Parsed Successfully:", signal);
        await executor.execute(signal);
    } else {
        console.log("// Could not parse signal.");
    }
}

main().catch(console.error);
