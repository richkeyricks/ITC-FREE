// ══════════════════════════════════════════════════════════════════════════════
// ⚡ EDGE FUNCTION: MIDTRANS WEBHOOK
// 🎯 ROLE: Securely receives payment notifications and updates Database
// ══════════════════════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"
import { crypto } from "https://deno.land/std@0.177.0/crypto/mod.ts";

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders })
    }

    try {
        // 1. Initialize Supabase Admin (Bypass RLS)
        const supabaseAdmin = createClient(
            Deno.env.get('SUPABASE_URL') ?? '',
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
        )

        // 2. Parse Midtrans Notification Payload
        const notification = await req.json()
        console.log("🔔 Midtrans Notification:", notification)

        const orderId = notification.order_id
        const transactionStatus = notification.transaction_status
        const fraudStatus = notification.fraud_status
        let newStatus = 'PENDING'

        // 3. Determine Status Logic (Standard Midtrans Rules)
        if (transactionStatus == 'capture') {
            if (fraudStatus == 'challenge') {
                newStatus = 'CHALLENGE'
            } else if (fraudStatus == 'accept') {
                newStatus = 'SUCCESS'
            }
        } else if (transactionStatus == 'settlement') {
            newStatus = 'SUCCESS'
        } else if (transactionStatus == 'cancel' || transactionStatus == 'deny' || transactionStatus == 'expire') {
            newStatus = 'FAILED'
        } else if (transactionStatus == 'pending') {
            newStatus = 'PENDING'
        }

        // 4. Update Database
        const { error } = await supabaseAdmin
            .from('marketplace_orders')
            .update({
                status: newStatus,
                payment_method: notification.payment_type, // Mapped to existing column
                fraud_status: fraudStatus,
                updated_at: new Date(),
                paid_at: newStatus === 'SUCCESS' ? new Date() : null
            })
            .eq('order_id', orderId)

        if (error) {
            throw error
        }

        // 5. If Success, Auto-Upgrade User (Optional Logic)
        if (newStatus === 'SUCCESS') {
            // Logic to auto-upgrade user tier based on preset_id can be added here
            // or handled by a Database Trigger.
            console.log(`✅ Order ${orderId} marked as SUCCESS`)
        }

        return new Response(JSON.stringify({ message: "OK", status: newStatus }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: 200,
        })

    } catch (error) {
        console.error("❌ Webhook Error:", error)
        return new Response(JSON.stringify({ error: error.message }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: 400,
        })
    }
})
