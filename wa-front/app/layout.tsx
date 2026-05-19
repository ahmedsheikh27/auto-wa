import type { Metadata } from "next";
import "./globals.css";
import Appbar from "./components/AppBar";

export const metadata: Metadata = {
  title: "AUTO-WA",
  description: "Whatsapp automation clone",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
    >
      <body className="min-h-full flex flex-col">
        <Appbar />
        {children}</body>
    </html>
  );
}
