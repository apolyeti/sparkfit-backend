"use client";

import { Metadata } from "next";
import FileInput from "@components/FileInput/FileInput";
import { SparkFitImage } from "@utils/types";
import Closet from "@components/Closet";
import { useState, useEffect } from "react";



// export const metadata: Metadata = {
//     title: "Sparkfit",
//     description: "Get outfit suggestions based on the weather",
// }

export default function Home() {

    const [images, setImages] = useState<SparkFitImage[]>([]);

    const loadImages = () => {
        const storedImages = localStorage.getItem("images");
        if (storedImages) {
            setImages(JSON.parse(storedImages));
        }
    };

    useEffect(() => {
        loadImages();
    }, []);

    const addImage = (image: SparkFitImage) => {
        const updatedImages = [...images, image];
        setImages(updatedImages);
        localStorage.setItem("images", JSON.stringify(updatedImages));
    };

    return (
        <>
            {/* create block design for home page */}
            <div className="flex flex-col items-center justify-center min-h-screen p-4">
                <h1 className="text-6xl font-bold">Sparkfit</h1>
                <button 
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    onClick={() => {
                        localStorage.clear();
                        setImages([]);
                    }
                }>   
                    Clear
                </button>
                <p className="text-1xl">Get outfit suggestions based on the weather</p>
                <div className="mt-8">
                    <FileInput addImage={addImage}/>
                </div>
                <div className="mt-8 w-full">
                    <Closet images={images}/>
                </div>
            </div>
        </>
    );
}
