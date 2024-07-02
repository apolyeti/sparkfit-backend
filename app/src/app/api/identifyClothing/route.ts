// import tensorflowjs-node
import * as tf from '@tensorflow/tfjs-node';
import * as fs from 'fs';
import {NextRequest, NextResponse} from 'next/server';

export async function POST(req: NextRequest, res: NextResponse) {
    const formData = await req.formData();

    const image = formData.get('image') as File;
    const name = formData.get('name') as string;

    return NextResponse.json({name: name});
}