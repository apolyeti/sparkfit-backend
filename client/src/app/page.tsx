import Image from "next/image";
import { Metadata } from "next";
import FileInput from "@components/FileInput/FileInput";

export const metadata: Metadata = {
    title: "Sparkfit",
    description: "Get outfit suggestions based on the weather",
}



export default function Home() {
  return (
    <>
        {/* create block design for home page */}
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-6xl font-bold">Sparkfit</h1>
            <p className="text-2xl">Get outfit suggestions based on the weather</p>
        </div>

        {/* create block design for file input */}
        <div className="flex flex-col items-center  h-screen">
            <FileInput />
        </div>

    </>
  );
}
