import tensorflow from '@tensorflow/tfjs';
import { type NextRequest, type NextResponse } from 'next/server';

// make post request to server
export async function POST(req: NextRequest, res: NextResponse) {
    // get image from request body
    const body = await req.json();
    const image = body.image;

    // load keras sequential model trained in python locally
    const model = await tensorflow.loadLayersModel('@models/classify_clothes.keras');

}