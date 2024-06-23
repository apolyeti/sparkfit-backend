"use client";
import Image from "next/image";
import { useDropzone } from "react-dropzone";

export default function Home() {
    const { getRootProps, getInputProps } = useDropzone();

    return (
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            <p>Upload photo here</p>
        </div>
    );
}
