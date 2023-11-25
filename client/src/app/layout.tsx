"use client";

import "./globals.css";
import type { Metadata } from "next";
import { redirect, usePathname, useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Inter } from "next/font/google";

import Cookies from "universal-cookie";
import { useEffect, useState } from "react";
import { User } from "@/models/User";

const cookies = new Cookies();

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [user, setUser] = useState(null as unknown as User);
  const [profilePic, setProfilePic] = useState("");

  useEffect(() => {
    setUser(cookies.get("user"));
    let profile = sessionStorage.getItem("profilePic");
    if (profile !== null && profile !== "null") {
      setProfilePic(profile);
    }
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
          {user && user.role === "admin" && <Link href="/admin">Admin</Link>}
          {user && user.role === "librarian" && (
            <Link href="/library">Library</Link>
          )}
          <div className="!ml-auto flex flex-wrap">
            {!user && <Link href="/login">Login</Link>}
            {user && (
              <Link href="/profile" className="mr-5">
                <img
                  src={profilePic ? profilePic : "/profile-img-placeholder.png"}
                  alt="Profile Picture"
                  className="rounded-full w-8 h-8"
                />
              </Link>
            )}
            {user && (
              <Link href="/login" onClick={logout}>
                Logout
              </Link>
            )}
          </div>
        </nav>
        <div className="mt-8">{children}</div>
      </body>
    </html>
  );
}
