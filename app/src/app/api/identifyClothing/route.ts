// import tensorflowjs-node
import * as tf from '@tensorflow/tfjs-node';
import * as fs from 'fs';
import {NextRequest, NextResponse} from 'next/server';

export async function POST(req: NextRequest, res: NextResponse) {
    const formData = await req.formData();

    const image = formData.get('image') as File;
    const name = formData.get('name') as string;
    console.log(name);

    const buffer = await image.arrayBuffer();
    // const tensor = tf.node.decodeImage(new Uint8Array(buffer));
//     // make the image 240x240
//     const resized = tf.image.resizeBilinear(tensor, [240, 240]);
//     const expanded = resized.expandDims(0);

    const modelPath = 
        'file://../tools/models/classify_clothes/classify_clothes.keras';
    // load the model
    // const model = await tf.loadLayersModel(modelPath);

    // // predict the image
    // const prediction = model.predict(expanded) as tf.Tensor;

    // const predictionData = prediction.dataSync();
    // const maxIndex = predictionData.indexOf(Math.max(...predictionData));

    // // get the label
    // const labels = fs.readFileSync(
    //     '../tools/models/classify_clothes/labels.txt', 'utf8');
    // const labelArray = labels.split('\n');
    // const label = labelArray[maxIndex];
    // console.log('predicted label:', label)

    const responseBody = {
        name: name
    };
    // responseData.append('label', label);



    return NextResponse.json(responseBody, {
        status: 200
    });
}