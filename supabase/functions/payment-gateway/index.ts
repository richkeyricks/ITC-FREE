// ══════════════════════════════════════════════════════════════════════════════
// 🏦 PAYMENT GATEWAY EDGE FUNCTION (MIDTRANS)
// 🛡️ SECURITY LEVEL: CRITICAL (ZERO-KNOWLEDGE)
// ══════════════════════════════════════════════════════════════════════════════
// 
// Role: Intermediary for signing transactions.
// Why: Keeps 'MIDTRANS_SERVER_KEY' safely in Cloud Environment (never in client).
// 
// Flow:
// 1. Client sends JWT + Order Data.
// 2. This function validates Session.
// 3. This function calls Midtrans Snap API.
// 4. Returns 'redirect_url' and 'token'.

// @ts-nocheck
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// --- CONSTANTS ---
const MIDTRANS_SANDBOX_URL = "https://app.sandbox.midtrans.com/snap/v1/transactions";
const MIDTRANS_PRODUCTION_URL = "https://app.midtrans.com/snap/v1/transactions";

const rawIsProduction = (Deno.env.get('MIDTRANS_IS_PRODUCTION') || '').toLowerCase().trim();
const isProduction = ['1', 'true', 'yes', 'production'].includes(rawIsProduction);
const MIDTRANS_API_URL = isProduction ? MIDTRANS_PRODUCTION_URL : MIDTRANS_SANDBOX_URL;

// --- CORS HEADERS ---
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
    // 1. Handle CORS Preflight
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders });
    }

    try {
        // 2. Auth Validation (Supabase JWT)
        const supabaseClient = createClient(
            Deno.env.get('SUPABASE_URL') ?? '',
            Deno.env.get('SUPABASE_ANON_KEY') ?? '',
            { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
        );

        const { data: { user }, error: authError } = await supabaseClient.auth.getUser();
        if (authError || !user) throw new Error("Unauthorized Access Detected");

        // 3. Parse Body
        const { order_id, amount, preset_name } = await req.json();
        if (!order_id || amount === undefined || amount === null) throw new Error("Missing Transaction Parameters");

        const parsedAmount = Number(amount);
        if (!Number.isFinite(parsedAmount) || parsedAmount <= 0) {
            throw new Error("Invalid Transaction Amount");
        }

        // 4. Idempotency Check (Prevent Double Charge)
        // Check if order_id already exists in database
        const { data: existingOrder } = await supabaseClient
            .from('marketplace_orders')
            .select('status')
            .eq('order_id', order_id)
            .single();

        if (existingOrder && existingOrder.status === 'PAID') {
            throw new Error("Order Already Paid. Idempotency Triggered.");
        }

        // 5. Build Midtrans Payload
        const serverKey = Deno.env.get('MIDTRANS_SERVER_KEY') ?? '';
        if (!serverKey) throw new Error("Server Configuration Error 500: Keys Missing");

        if (isProduction && serverKey.startsWith('SB-')) {
            throw new Error("Production mode is enabled, but MIDTRANS_SERVER_KEY is still Sandbox (SB-)");
        }

        const authString = btoa(serverKey + ":"); // Basic Auth

        const payload = {
            transaction_details: {
                order_id: order_id,
                gross_amount: Math.round(parsedAmount), // Integer IDR
            },
            credit_card: { secure: true },
            item_details: [
                {
                    id: order_id,
                    price: Math.round(parsedAmount),
                    quantity: 1,
                    name: `Unlock: ${preset_name || 'Premium Strategy'}`,
                }
            ],
            customer_details: {
                first_name: "Trader",
                email: user.email,
                phone: user.phone || "08123456789", // Fallback required by Midtrans
            }
        };

        // 6. Call Midtrans API
        const mtResponse = await fetch(MIDTRANS_API_URL, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Basic ${authString}`
            },
            body: JSON.stringify(payload),
        });

        const mtData = await mtResponse.json();

        if (!mtResponse.ok) {
            console.error("Midtrans Error:", mtData);
            throw new Error(`Payment Gateway Error: ${mtData.error_messages?.[0] || 'Unknown'}`);
        }

        // 7. Secure Return
        return new Response(JSON.stringify({
            token: mtData.token,
            redirect_url: mtData.redirect_url,
            status: "success"
        }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });

    } catch (error) {
        console.error("Function Error:", error);
        return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
    }
});
