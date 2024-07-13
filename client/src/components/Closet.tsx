"use client";

import ClothingItem from "@components/ClothingItem";
import type { SparkFitImage } from "@utils/types";
import { useState, useEffect } from "react";


interface ClosetProps {
    images: SparkFitImage[];
}

export default function Closet({images} : ClosetProps){

    
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