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
        <>
            <div className="closet-container">
                <div className="image-grid">
                    {images.map((image) => (
                        <ClothingItem key={image.name} image={image} />
                    ))}
                </div>
            </div>
            <style jsx>{`
                .closet-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    overflow-y: auto;
                    max-height: 100vh;
                    width: 100%;
                    padding: 16px;
                }
                .image-grid {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 16px;
                }
                .image-container {
                    max-width: 200px;
                    max-height: 200px;
                    overflow: hidden;
                }
                .image-container img {
                    width: 100%;
                    height: auto;
                }
            `}</style>
        </>
    )
}