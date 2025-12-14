"use client";
import { Suspense, useState } from "react";
import Dropzone from "./components/DropZone";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [videoSrc, setVideoSrc] = useState(" ");
  const handleSetFile = (file: File[]) => {
    setFiles(file);
  };

  const submitData = async (formData: FormData) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        "http://localhost:5023/api/Convert/AddSubtitle",
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const body = await response.blob();
        const url = URL.createObjectURL(body);
        setVideoSrc(url);
        setFiles([]);
        setIsLoading(false);
      } else {
        console.error("error");
        setFiles([]);
      }
    } catch (err) {
      console.error(err);
      setFiles([]);
    }
  };

  return (
    <div className="bg-white w-screen flex justify-center items-center flex-col gap-10">
      <link
        rel="icon"
        href={isLoading ? "/favicon.gif" : "/vercel.svg"}
        type="image/gif"
      />

      <iframe src={videoSrc}></iframe>

      <div className="relative border-4 border-black size-fit hover:cursor-pointer hover:bg-black hover:text-white duration-200 ease-out uppercase">
        <Dropzone
          files={files}
          setFiles={handleSetFile}
          submitData={submitData}
        ></Dropzone>
      </div>
    </div>
  );
}
