"use client";

import "./globals.css";
import type { Metadata } from "next";
import { redirect, usePathname, useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Inter } from "next/font/google";

import Cookies from "universal-cookie";
import { useEffect, useState } from "react";

const cookies = new Cookies();

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(cookies.get("user"));
  }, [pathname, searchParams]);

  function logout() {
    cookies.set("user", null);
  }

  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="top-0 bg-gray-400 p-6 flex flex-wrap space-x-7">
          <Link href="/">Home</Link>
          {user && <Link href="/catalog">Catalog</Link>}
          {user && <Link href="/admin">Admin</Link>}
          {!user && (
            <Link href="/login" className="!ml-auto">
              Login
            </Link>
          )}
          {user && (
            <Link href="/login" onClick={logout} className="!ml-auto">
              Logout
            </Link>
          )}
        </nav>
        <div className="mt-8">{children}</div>
      </body>
    </html>
  );
}
