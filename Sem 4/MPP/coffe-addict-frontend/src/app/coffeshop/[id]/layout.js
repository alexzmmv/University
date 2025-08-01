import { Geist, Geist_Mono } from "next/font/google";
import "../../styles/globals.css";
import { Header } from "@/app/components/coffeShopPage/Header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function Layout({ children }) {
  return (
    <>
      <Header />
      <div
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[var(--background)] text-[var(--foreground)] min-h-screen`}
      >
        {children}
      </div>
    </>
  );
}
