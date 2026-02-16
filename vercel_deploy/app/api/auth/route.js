import { NextResponse } from 'next/server';

export async function POST(request) {
    try {
        const body = await request.json();
        const { pin } = body;
        const MASTER_PIN = process.env.COMMANDER_MASTER_PIN;

        if (!MASTER_PIN) {
            console.error('SERVER ERROR: COMMANDER_MASTER_PIN is undefined.');
            return NextResponse.json({ authorized: false, message: 'SERVER ERROR: ENV NOT SET' }, { status: 500 });
        }

        // Use trim() to avoid mismatch if user or ENV has extra spaces
        if (pin?.toString().trim() === MASTER_PIN.trim()) {
            return NextResponse.json({ authorized: true }, { status: 200 });
        } else {
            return NextResponse.json({ authorized: false, message: 'INCORRECT PIN' }, { status: 401 });
        }
    } catch (err) {
        return NextResponse.json({ authorized: false, message: 'Internal Server Error' }, { status: 500 });
    }
}

export async function OPTIONS() {
    return NextResponse.json({}, { status: 200 });
}
