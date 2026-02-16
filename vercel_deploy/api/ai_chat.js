export default async function handler(req, res) {
    // Only allow POST
    if (req.method !== "POST") {
        return res.status(405).json({ error: "Method Not Allowed" });
    }

    try {
        const { message, userContext } = req.body;

        // Use Vercel Env or Fallback to Master Key
        const MASTER_KEY = "";
        const apiKey = process.env.GROQ_API_KEY || MASTER_KEY;

        if (!apiKey) {
            return res.status(500).json({ error: "Server Configuration Error: API Key missing." });
        }

        // Construct System Prompt with Live Context
        const systemPrompt = `
You are the "ITC AI Companion", an expert trading assistant for the ITC +AI Enterprise system.
Your goal is to help the user based on their REAL-TIME trading data.

USER CONTEXT:
- Name: ${userContext.name || "Trader"}
- Broker: ${userContext.broker || "Unknown"}
- Balance: ${userContext.balance || "$0"}
- Equity: ${userContext.equity || "$0"}
- Total Profit/Loss: ${userContext.profit || "$0"}

INSTRUCTIONS:
1. Answer short, concise, and professional.
2. Use the provided context to give personalized advice.
3. Do not mention you are an AI model. You are part of the ITC system.
4. Language: Indonesian (unless user speaks English).
        `.trim();

        // Call Groq API
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama3-8b-8192",
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: message }
                ],
                temperature: 0.7
            })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error.message);
        }

        return res.status(200).json({ reply: data.choices[0].message.content });

    } catch (error) {
        return res.status(500).json({ error: "AI Error: " + error.message });
    }
}
