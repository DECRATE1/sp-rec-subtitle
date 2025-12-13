"use client";

import { useCallback, useState } from "react";

export default function Dropzone({
  files,
  setFiles,
}: {
  files: File[];
  setFiles: (file: File[]) => void;
}) {
  const [title, setTitle] = useState("Перетащите файл или выберите");
  const onDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      const dropped = Array.from(e.dataTransfer.files || []);
      setFiles([...dropped]);
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
      {title}
      <input
        type="file"
        multiple
        style={{ display: "none" }}
        onChange={(e) => setFiles(Array.from(e.target.files || []))}
      />
    </div>
  );
}
