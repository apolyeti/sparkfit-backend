"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function FileInput() {

    const onDrop = useCallback((acceptedFiles : File[]) => {
        // Do something with the files
        console.log(acceptedFiles)
      }, [])

    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

    return (
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            {
                isDragActive ?
                <p>Drop the files here ...</p> :
                <p>Drag 'n' drop some files here, or click to select files</p>
            }
        </div>
    )
}