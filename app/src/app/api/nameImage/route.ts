import { NextResponse, type NextRequest } from 'next/server';

export async function POST(req: NextRequest, res: NextResponse) {
    // get name from request body
    const body = await req.json();

    return NextResponse.json({ name: body.name });
}