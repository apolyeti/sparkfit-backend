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

        reader.onload = async () => {
            // get image data 
            const imageData = reader.result as string;
            setImage(imageData);
            const fileName = file.name;

            const formData = new FormData();
            formData.append('image', file);
            formData.append('name', fileName);

            try {
                const response = await fetch('/api/identifyClothing', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    setName(data.name);
                } else {
                    console.error('Failed to get name');
                }
            } catch (error) {
                console.error('Failed to get name', error);
            }
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
