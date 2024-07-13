
import { Metadata } from "next";
import FileInput from "@components/FileInput/FileInput";
import { SparkFitImage } from "@utils/types";
import Closet from "@components/Closet";



export const metadata: Metadata = {
    title: "Sparkfit",
    description: "Get outfit suggestions based on the weather",
}

export default function Home() {
    return (
        <>
            {/* create block design for home page */}
            <div className="flex flex-col items-center justify-center min-h-screen p-4">
                <h1 className="text-6xl font-bold">Sparkfit</h1>
                <p className="text-1xl">Get outfit suggestions based on the weather</p>
                <div className="mt-8">
                    <FileInput />
                </div>
                <div className="mt-8 w-full">
                    <Closet />
                </div>
            </div>
        </>
    );
}
