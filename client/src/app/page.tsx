import Image from "next/image";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Sparkfit",
    description: "Get outfit suggestions based on the weather",
}



export default function Home() {
  return (
    <>
        <h1 className="text-4xl font-bold">
            Sparkfit
        </h1>
        {/* add spacer here */}
        <span className="block h-4"></span>
        <p>Get outfit suggestions based on the weather</p>
    </>
  );
}
