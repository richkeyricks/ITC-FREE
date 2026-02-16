import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

Deno.serve(async (req) => {
    try {
        const dow = new Date().getDay();
        // Friday Protocol: Only runs on Day 5 (Friday)
        if (dow !== 5) {
            return new Response(JSON.stringify({ message: "Quantum Payout Protocol: Standard Operation. Waiting for Friday." }), { status: 200 });
        }

        const supabase = createClient(
            Deno.env.get('SUPABASE_URL') ?? '',
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
        );

        // 1. Fetch all Requested Payouts >= 1,000,000 IDR
        const { data: payouts, error } = await supabase
            .from('payout_requests')
            .select('*')
            .eq('status', 'REQUESTED')
            .gte('amount', 1000000);

        if (error) throw error;

        // 2. Logic: Process transfers (Integration with Bank API or Admin Notification)
        // For this engine: We mark them as 'PROCESSING' for admin batching
        if (payouts && payouts.length > 0) {
            const ids = payouts.map(p => p.id);
            await supabase.from('payout_requests').update({ status: 'PROCESSING' }).in('id', ids);

            return new Response(JSON.stringify({
                message: "Quantum Friday Protocol: Payouts Batched.",
                count: payouts.length
            }), { status: 200 });
        }

        return new Response("No eligible payouts found.", { status: 200 });

    } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
});
