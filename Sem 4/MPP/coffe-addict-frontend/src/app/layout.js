'use client';

import { Geist, Geist_Mono } from "next/font/google";
import "./styles/globals.css";
import { ApiUrlProvider } from "./utils/ApiUrlContext";
import { AuthProvider } from "./utils/AuthContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <ApiUrlProvider>
            <main>
              {children}
            </main>
          </ApiUrlProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
