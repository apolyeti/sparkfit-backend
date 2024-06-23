"use client";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";

export default function Home() {

    const [image, setImage] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles : File[]) => {
        acceptedFiles.forEach((file) => {
            const reader = new FileReader();

            reader.onabort = () => console.log("file reading was aborted");
            reader.onerror = () => console.log("file reading has failed");

            reader.onload = () => {
                // save the image to images/ folder
                setImage(reader.result as string);
            }
            reader.readAsDataURL(file);
        })
    }, []);

    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            <p>Upload photo here</p>

            <div id="imageDisplay">
                {image && 
                    <Image 
                        src={image} alt="uploaded image" 
                        width={200} height={200}
                    />
                }
            </div>
        </div>
    );
}
