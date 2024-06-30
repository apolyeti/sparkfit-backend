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
            if (reader.result) {
                const base64Image = reader.result.toString().split(',')[1]; // Extract the base64 part
                fetch("/api/identifyClothing", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ 
                    image: base64Image,
                    fileName: file.name,
                   }), // Send base64 part only
                })
                  .then((res) => res.json())
                  .then((data) => {
                    if (data.name) {
                      setName(data.name as string);
                    }
                  });
                
                const url = URL.createObjectURL(file);
                setImage(url);
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
