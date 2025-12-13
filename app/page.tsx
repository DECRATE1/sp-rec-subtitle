"use client";
import { useEffect, useState } from "react";
import Dropzone from "./components/DropZone";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  const handleSetFile = (file: File[]) => {
    setFiles(file);
  };

  useEffect(() => {}, [files]);
  return (
    <div className="bg-white w-screen flex justify-center items-center">
      <link
        rel="icon"
        href={isLoading ? "/favicon.gif" : "/vercel.svg"}
        type="image/gif"
      />
      <div className="border-4 border-black size-fit hover:cursor-pointer hover:bg-black hover:text-white duration-200 ease-out uppercase">
        <Dropzone files={files} setFiles={handleSetFile}></Dropzone>
      </div>
    </div>
  );
}
