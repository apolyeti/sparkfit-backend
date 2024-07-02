// import tensorflowjs-node
import * as tf from '@tensorflow/tfjs-node';
import * as fs from 'fs';
import {NextRequest, NextResponse} from 'next/server';

export async function POST(req: NextRequest, res: NextResponse) {
    const body = await req.json();
    const image = body.image;

    // process the image first
    
    // load the model
    const model = await tf.loadLayersModel('file://path/to/model.json');

    return NextResponse.json({ name: 'name' });
}