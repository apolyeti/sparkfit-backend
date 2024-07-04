"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import type { SparkFitImage } from "@utils/types";

interface FileInputProps {
    onImageUpload: (image: SparkFitImage) => void;
}

export default function FileInput(FileInputProps: FileInputProps) {

    const onDrop = useCallback((acceptedFiles : File[]) => {
        // get each file
        const file = acceptedFiles[0];

        const reader = new FileReader();

        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.onload = async () => {
            const formData = new FormData();
        }


    }, []);

    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

    return (
        <div {...getRootProps()} className="border-2 border-dashed border-gray-40 p-4 w-full text-center">
            <input {...getInputProps()} />
            {
                isDragActive ?
                <p>Drop the files here ...</p> :
                <p>Drag 'n' drop some files here, or click to select files</p>
            }
        </div>
    )
}