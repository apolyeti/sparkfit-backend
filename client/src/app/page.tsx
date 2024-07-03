import Image from "next/image";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Sparkfit",
    description: "Get outfit suggestions based on the weather",
}



export default function Home() {
  return (
    <div>
      <h1>Sparkfit</h1>
      <p>Get outfit suggestions based on the weather</p>
    </div>    
  );
}
