// import tensorflowjs-node
import * as tf from '@tensorflow/tfjs-node';
import * as fs from 'fs';
import {NextRequest, NextResponse} from 'next/server';

export async function POST(req: NextRequest, res: NextResponse) {
    const body = await req.json();
    console.log(body);
    return NextResponse.json({ name: body.name });
}