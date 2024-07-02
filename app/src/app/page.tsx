"use client";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";

export default function Home() {

    const [image, setImage] = useState<string | null>(null);
    const [name, setName] = useState<string>("");

    const onDrop = useCallback((acceptedFiles : File[]) => {
        const file = acceptedFiles[0];
        const reader = new FileReader();

        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.onload = () => {
            // get image data
        };

        reader.readAsDataURL(file);
    }, []);

    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            <p>Upload photo here {name}</p>

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
