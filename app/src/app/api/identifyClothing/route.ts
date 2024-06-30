import * as tf from '@tensorflow/tfjs-node';
import {  NextRequest,  NextResponse } from 'next/server';
import * as path from 'path';
import * as fs from 'fs';


// function to get class names from directory
function getClassNamesFromDirectory(directory: string) {
    // each class name is the name of a subdirectory in the directory
    const classNames = fs.readdirSync(directory);
    return classNames;
}

// make post request to server
export async function POST(req: NextRequest, res: NextResponse) {

    // get image from request body
    const body = await req.json();
    console.log("HELLO WE GOT HERE");
    console.log(body);
    const image = body.image;



    // load keras sequential model trained in python locally
    const modelPath = path.resolve('../../../../../tools/models/classify_clothes.keras');
    const model = await tf.loadLayersModel('file://' + modelPath);

    // preprocess image
    const tensor = tf.browser.fromPixels(image);
    const resized = tf.image.resizeBilinear(tensor, [224, 224]);
    const expanded = resized.expandDims(0);
    const preprocessed = expanded.toFloat().div(255);

    // predict image
    const prediction = model.predict(preprocessed) as tf.Tensor;

    const predictionData = await prediction.data();
    const predictedClassIndex = tf.argMax(predictionData).dataSync()[0];
    const classNames = getClassNamesFromDirectory('../../../../../tools/data/clothes/')

    return NextResponse.json({ name: classNames[predictedClassIndex] });
}