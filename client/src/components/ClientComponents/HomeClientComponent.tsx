"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import type { SparkFitImage } from "@utils/types";
import FileInput from "../FileInput/FileInput";

export default function HomeClientComponent() {
    const [images, setImages] = useState<SparkFitImage[]>([]);

    useEffect(() => {
        // Load images from local storage on component mount
        const storedImages = JSON.parse(localStorage.getItem("images") || "[]");
        setImages(storedImages);
    }, []);

    const handleImageUpload = (image: SparkFitImage) => {
        // Save image to local storage
        const images = JSON.parse(localStorage.getItem("images") || "[]");
        images.push(image);
        localStorage.setItem("images", JSON.stringify(images));
        setImages(images);
    };

    return (
        <div className="flex flex-col items-center w-full">
            <FileInput onImageUpload={handleImageUpload} />
            <div className="flex flex-wrap justify-center mt-4">
            {images.map((image, index) => (
                <Image key={index} src={image.data} alt={image.name} width={200} height={200} />
            ))}
            </div>
        </div>
    );
}
