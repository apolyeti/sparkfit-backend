"use client";

import ClothingItem from "@components/ClothingItem";
import type { SparkFitImage } from "@utils/types";
import { useState, useEffect } from "react";


export default function Closet() {

    const [images, setImages] = useState<SparkFitImage[]>([]);

    const loadImages = () => {
        const storedImages = localStorage.getItem("images");
        if (storedImages) {
            setImages(JSON.parse(storedImages));
        }
    }

    useEffect(() => {
        loadImages();

        const handleStorageChange = (event: StorageEvent) => {
            if (event.key === "images") {
                loadImages();
            }
        }

        window.addEventListener("storage", handleStorageChange);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
        }
        
    }, []);

    
    return (
        <div className="flex flex-col items-center justify-center">
            {images.map((image) => (
                <ClothingItem key={image.name} image={image} />
            ))}
        </div>
    )
}