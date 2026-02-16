import { ImageResponse } from '@vercel/og';

export const runtime = 'edge';

export async function GET(request) {
    try {
        const { searchParams } = new URL(request.url);

        // Dynamic Params
        const profit = searchParams.get('profit') || '1000';
        const pair = searchParams.get('pair') || 'XAUUSD';
        const user = searchParams.get('user') || 'Trader';

        // Premium Design Logic
        return new ImageResponse(
            (
                <div
                    style={{
                        height: '100%',
                        width: '100%',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        backgroundColor: '#0a0a0a',
                        fontFamily: 'sans-serif',
                        color: 'white',
                        backgroundImage: 'linear-gradient(to bottom right, #000000, #111111)',
                    }}
                >
                    {/* Glowing Border Effect */}
                    <div
                        style={{
                            position: 'absolute',
                            top: '20px',
                            left: '20px',
                            right: '20px',
                            bottom: '20px',
                            border: '2px solid #D4AF37', // Gold
                            borderRadius: '20px',
                            opacity: 0.3,
                        }}
                    />

                    {/* User Handling */}
                    <div style={{ fontSize: 30, color: '#888', marginBottom: 20 }}>
                        {user} just profited
                    </div>

                    {/* Massive Profit Number */}
                    <div
                        style={{
                            fontSize: 120,
                            fontWeight: 900,
                            background: 'linear-gradient(to bottom, #D4AF37, #AA8C2C)',
                            backgroundClip: 'text',
                            color: 'transparent',
                            textShadow: '0 0 40px rgba(212, 175, 55, 0.4)',
                            lineHeight: 1,
                        }}
                    >
                        ${profit}
                    </div>

                    {/* Pair Info */}
                    <div
                        style={{
                            marginTop: 40,
                            display: 'flex',
                            alignItems: 'center',
                            backgroundColor: '#222',
                            padding: '10px 30px',
                            borderRadius: '50px',
                            border: '1px solid #333',
                        }}
                    >
                        <span style={{ fontSize: 30, color: '#aaa', marginRight: 10 }}>ON</span>
                        <span style={{ fontSize: 30, fontWeight: 'bold', color: 'white' }}>{pair}</span>
                    </div>

                    {/* Footer Branding */}
                    <div style={{ position: 'absolute', bottom: 40, fontSize: 20, color: '#555' }}>
                        Powered by Haineo Global Systems
                    </div>
                </div>
            ),
            {
                width: 1200,
                height: 630,
            }
        );
    } catch (e) {
        return new Response(`Failed to generate the image`, {
            status: 500,
        });
    }
}
