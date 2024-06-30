"use client";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";

export default function Home() {

    const [image, setImage] = useState<string | null>(null);
    const [name, setName] = useState<string>("");

    const onDrop = useCallback((acceptedFiles : File[]) => {
        acceptedFiles.forEach((file) => {
            const reader = new FileReader();
            const formData = new FormData();
            formData.append('image', file);

            fetch("/api/identifyClothing", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ image: reader.result }),
            })
            .then((res) => res.json())
            .then((data) => setName(data.name as string));

            reader.onabort = () => console.log("file reading was aborted");
            reader.onerror = () => console.log("file reading has failed");

            reader.readAsDataURL(file);
            reader.onload = () => {
                // make post request to nameImage
                // fetch("/api/nameImage", {
                //     method: "POST",
                //     headers: {
                //         "Content-Type": "application/json",
                //     },
                //     body: JSON.stringify({ name: file.name }),
                // })
                // .then((res) => res.json())
                // // .then((data) => setName(data.name as string));

                // make post request to identifyClothing
                const url = URL.createObjectURL(file);
                setImage(url);

            }
        })
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
