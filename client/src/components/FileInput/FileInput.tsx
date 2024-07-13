"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import type { SparkFitImage } from "@utils/types";

export default function FileInput({ addImage }: { addImage: (image: SparkFitImage) => void }) {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];

        const reader = new FileReader();

        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.onload = async () => {
            const formData = new FormData();
            
            formData.append('file', file);
            formData.append('name', file.name);
            
            try {
                const response = await fetch("/api/classifyClothing", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Failed to upload image");
                }
                const data = await response.json();
                console.log(data);

                const newImage: SparkFitImage = {
                    name: data.predictions[0],
                    data: reader.result as string,
                    file_name: file.name
                };

                addImage(newImage);

            } catch (error) {
                console.error(error);
            }
        }
        reader.readAsDataURL(file);
    }, [addImage]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
        <div {...getRootProps({ className: 'dropzone' })}>
            <input {...getInputProps()} />
            {
                isDragActive ?
                <p>Drop the files here ...</p> :
                <p>Drag and drop some files here, or click to select files</p>
            }
            <style jsx>{`
                .dropzone {
                    border: 2px dashed #cccccc;
                    padding: 20px;
                    text-align: center;
                    cursor: pointer;
                    transition: border 0.3s ease-in-out, background-color 0.3s ease-in-out;
                }
                .dropzone:hover {
                    border-color: #aaaaaa;
                    background-color: #f0f0f0;
                }
            `}</style>
        </div>
    );
}
