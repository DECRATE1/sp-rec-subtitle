"use client";

import { useCallback, useRef, useState } from "react";

export default function Dropzone({
  files,
  setFiles,
  submitData,
}: {
  files: File[];
  setFiles: (file: File[]) => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  submitData: (formData: any) => void;
}) {
  const [title, setTitle] = useState("Перетащите файл или выберите");
  const formRef = useRef<HTMLFormElement>(null);
  const onDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      const dropped = Array.from(e.dataTransfer.files || []);
      setFiles([...dropped]);
      if (!formRef.current) return;
      formRef.current.requestSubmit();
    },
    [setFiles]
  );

  const onDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  return (
    <div
      onDrop={onDrop}
      onDragOver={onDragOver}
      className="p-6 text-center duration-400 ease-out select-none"
      style={{
        background: files.length > 0 ? "black" : "white",
        color: files.length > 0 ? "white" : "black",
      }}
    >
      <form
        action={async (formData) => await submitData(formData)}
        ref={formRef}
        className="w-full h-full"
      >
        {title}
        <input
          type="file"
          name="video"
          multiple
          className="absolute text-transparent left-0 w-full h-full top-0 cursor-pointer"
          accept="video/mp4"
          onChange={(e) => {
            setFiles(Array.from(e.target.files || []));
            formRef.current?.requestSubmit();
          }}
        />
      </form>
    </div>
  );
}
