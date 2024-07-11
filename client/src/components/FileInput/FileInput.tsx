"use client";

import { useCallback, useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";
import type { SparkFitImage } from "@utils/types";


export default function FileInput() {

    const [images, setImages] = useState<SparkFitImage[]>([]);

    useEffect(() => {
        const storedImages = localStorage.getItem("images");
        if (storedImages) {
            setImages(JSON.parse(storedImages));
        }
    }
    , []);




    const onDrop = useCallback((acceptedFiles : File[]) => {
        // get each file
        const file = acceptedFiles[0];

        const reader = new FileReader();

        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.onload = async () => {
            const formData = new FormData();
            
            formData.append('file', file);
            formData.append('name', file.name);
            
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

                const newImage : SparkFitImage = {
                    name: data.predictions[0],
                    // url for Image src
                    data: URL.createObjectURL(file),
                    file_name: file.name
                }
                
                const updatedImages = [...images, newImage];
                setImages(updatedImages);
                localStorage.setItem("images", JSON.stringify(updatedImages));

            } catch (error) {
                console.error(error);
            }
            
        }
        reader.readAsDataURL(file);

    }, [images]);

    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

    return (
        <>
            <div {...getRootProps()} className="border-2 border-dashed border-gray-40 p-4 w-full text-center">
                <input {...getInputProps()} />
                {
                    isDragActive ?
                    <p>Drop the files here ...</p> :
                    <p>Drag and drop some files here, or click to select files</p>
                }
            </div>
        </>
    )
}