export const revalidate = 86400; // Cache for 24 hours (ISR Smart Caching)

export async function generateMetadata({ params }) {
    const { userId, profit } = params;

    // Construct the OG Image URL
    // In production, use the actual domain. For Vercel, relative URLs in metadata need full path or process.env.VERCEL_URL
    const baseUrl = process.env.VERCEL_URL
        ? `https://${process.env.VERCEL_URL}`
        : 'http://localhost:3000';

    // Clean up params
    const cleanProfit = profit.replace(/[^0-9.]/g, ''); // Security sanitization
    const cleanUser = userId.substring(0, 20); // Length limit

    const ogUrl = `${baseUrl}/api/og?profit=${cleanProfit}&user=${cleanUser}&pair=XAUUSD`;

    return {
        title: `💰 $${cleanProfit} Profit by ${cleanUser} | Haineo Success`,
        description: `Check out this massive trade execution by ${cleanUser} using Haineo Copytrade.`,
        openGraph: {
            title: `💰 $${cleanProfit} Profit on Haineo`,
            description: `Verified Market Execution. Join the elite.`,
            images: [
                {
                    url: ogUrl,
                    width: 1200,
                    height: 630,
                },
            ],
        },
        twitter: {
            card: 'summary_large_image',
            title: `💰 $${cleanProfit} Profit on Haineo`,
            description: `Verified Market Execution.`,
            images: [ogUrl],
        },
    };
}

export default function Page({ params }) {
    const { userId, profit } = params;

    return (
        <div style={{
            minHeight: '100vh',
            backgroundColor: '#050505',
            color: 'white',
            fontFamily: 'sans-serif',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            padding: '20px'
        }}>
            {/* Hero Section */}
            <h1 style={{
                fontSize: '4rem',
                background: 'linear-gradient(to right, #fff, #888)',
                backgroundClip: 'text',
                color: 'transparent',
                marginBottom: '10px'
            }}>
                {userId} just made ${profit}
            </h1>

            <p style={{ color: '#666', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 40px' }}>
                Verified execution via Haineo AI Copytrade System. The market yielded to their strategy.
            </p>

            {/* Call to Action - convert the viewer */}
            <a href="https://t.me/YourTelegramChannel" style={{
                padding: '15px 40px',
                backgroundColor: 'white',
                color: 'black',
                borderRadius: '50px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1.1rem',
                transition: 'opacity 0.2s',
                marginBottom: '20px'
            }}>
                Start Copytrading Free
            </a>

            <div style={{ marginTop: '50px', borderTop: '1px solid #333', paddingTop: '20px' }}>
                <p style={{ fontSize: '0.8rem', color: '#444' }}>
                    Haineo Global Systems &copy; 2026
                </p>
            </div>
        </div>
    );
}
