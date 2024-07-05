"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import type { SparkFitImage } from "@utils/types";


export default function FileInput() {

    const onDrop = useCallback((acceptedFiles : File[]) => {
        // get each file
        const file = acceptedFiles[0];

        const reader = new FileReader();

        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.onload = async () => {
            const formData = new FormData();
            // request body needs
            // name of image
            // data of image
            formData.append("name", file.name);
            formData.append("data", reader.result as string);
            
            try {
                const response = await fetch("api/classifyClothing", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Failed to upload image");
                }
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error(error);
            }
            
        }
        reader.readAsDataURL(file);

    }, []);

    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

    return (
        <div {...getRootProps()} className="border-2 border-dashed border-gray-40 p-4 w-full text-center">
            <input {...getInputProps()} />
            {
                isDragActive ?
                <p>Drop the files here ...</p> :
                <p>Drag and drop some files here, or click to select files</p>
            }
        </div>
    )
}