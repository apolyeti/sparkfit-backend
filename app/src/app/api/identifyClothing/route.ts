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
export async function POST(req: NextRequest) {
    console.log('hi')
    // get image from request body
    const body = await req.json();
    console.log("HELLO WE GOT HERE");

    // download image
    const base64Image = body.image;
    const fileName = body.fileName;
    const imageBuffer = Buffer.from(base64Image, 'base64');
    fs.writeFileSync('src/app/api/identifyClothing/image.jpg', imageBuffer);




    
    return NextResponse.json({ name: fileName });
}