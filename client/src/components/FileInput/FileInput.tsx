"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";
import type { SparkFitImage } from "@utils/types";


export default function FileInput() {

    const [image, setImage] = useState<SparkFitImage | null>(null);

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
                    name: data.description,
                    // url for Image src
                    data: URL.createObjectURL(file),
                    file_name: file.name
                }

                setImage(newImage);

            } catch (error) {
                console.error(error);
            }
            
        }
        reader.readAsDataURL(file);

    }, []);

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
            {image && (
                <div className="mt-4 flex flex-col items-center">
                    <Image src={image.data} width={200} height={200} alt={image.name} />
                    {/* make span go horizontally */}
                    <span className="flex flex-col items-center mt-2"> 
                        {/* make image name bold */}
                        <p className="text-xl">{image.name}</p>
                        {/* make file name grey and italicized */}
                        <p className="text-gray-50 italic">{image.file_name}</p>
                    </span>
                </div>
            )}
        </>
    )
}