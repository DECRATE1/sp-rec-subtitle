import "./globals.css";
import Header from "./components/Header";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="flex justify-center items-center flex-col bg-black overflow-hidden">
        <Header></Header>
        <main className="flex max-w-360 max-h-full w-screen h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
