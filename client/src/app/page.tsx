import { Metadata } from "next";
import HomeWrapper from "@components/HomeWrapper";

export const metadata: Metadata = {
    title: "Sparkfit",
    description: "Get outfit suggestions based on the weather",
}

export default function Home() {
    return (
        <>
            <HomeWrapper />
        </>
    );
}
