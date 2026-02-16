// src/modules/parser/signal-parser.service.ts
import { SIGNAL_REGEX } from '../../constants';

export interface SignalData {
    symbol: string;
    action: 'BUY' | 'SELL';
    entry?: number;
    sl?: number;
    tp: number[];
    extraInfo?: string;
}

export class SignalParserService {
    /**
     * Main parsing method
     */
    public parse(text: string): SignalData | null {
        try {
            const symbol = this.extractSymbol(text);
            const action = this.extractAction(text);
            const prices = this.extractPrices(text);

            if (!symbol || !action || prices.length < 2) {
                console.error(`// Parsing failed: Incomplete data in message: "${text}"`);
                return null;
            }

            // --- LOGIC: Identify which price is Entry, SL, and TP ---
            // Usually: First price is Entry, Second is SL or TP. 
            // We look for keywords like "SL", "Stop Loss", "TP", "Take Profit"

            const sl = this.extractStopLoss(text, prices);
            const entry = this.extractEntry(text, prices);
            const tp = this.extractTakeProfits(text, prices, sl, entry);

            return {
                symbol: symbol.toUpperCase(),
                action: action as 'BUY' | 'SELL',
                entry,
                sl,
                tp,
            };
        } catch (error) {
            console.error(`// Error in SignalParserService:`, error);
            return null;
        }
    }

    // --- PRIVATE HELPERS ---

    private extractSymbol(text: string): string | null {
        const match = text.match(SIGNAL_REGEX.SYMBOL);
        return match ? match[0] : null;
    }

    private extractAction(text: string): string | null {
        const match = text.match(SIGNAL_REGEX.ACTION);
        if (!match) return null;
        const action = match[0].toUpperCase();
        if (['BUY', 'LONG'].includes(action)) return 'BUY';
        if (['SELL', 'SHORT'].includes(action)) return 'SELL';
        return null;
    }

    private extractPrices(text: string): number[] {
        const matches = text.match(SIGNAL_REGEX.PRICE);
        return matches ? matches.map(Number) : [];
    }

    private extractStopLoss(text: string, prices: number[]): number | undefined {
        // Look for SL keyword and nearby number
        const slMatch = text.match(/(?:SL|Stop Loss)\D*(\d+(?:\.\d+)?)/i);
        return slMatch ? Number(slMatch[1]) : prices[1]; // Fallback to 2nd price
    }

    private extractEntry(text: string, prices: number[]): number | undefined {
        const entryMatch = text.match(/(?:Entry|Price|At|@)\D*(\d+(?:\.\d+)?)/i);
        return entryMatch ? Number(entryMatch[1]) : prices[0]; // Fallback to 1st price
    }

    private extractTakeProfits(text: string, prices: number[], sl?: number, entry?: number): number[] {
        // Filter out entry and sl from the list of numbers found
        return prices.filter(p => p !== sl && p !== entry);
    }
}
