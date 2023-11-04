"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { User } from "@/models/User";
import { Library } from "@/models/Library";
const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null as unknown as User);
  const [library, setLibrary] = useState(null as unknown as Library);

  const server = "http://127.0.0.1:5001/";
  useEffect(() => {
    let userCookie: User = cookies.get("user");
    if (!userCookie || userCookie.role !== "librarian") {
      redirect("/");
    } else {
      setUser(userCookie);
    }
    if (user) {
      fetch(server + "library?user=" + user.id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            throw Error("Failed to get catalog");
          }
        })
        .then((lib) => setLibrary(lib))
        .catch((error: Error) => console.log(error));
    }
  }, []);

  function formatCategory(type: string) {
    if (type === "book") {
      return "Book";
    } else if (type === "movie") {
      return "Movie";
    } else if (type === "videoGame") {
      return "Video Game";
    }
    return "Unknown";
  }

  return (
    <div className="text-center">
      <h1>Your Library</h1>
    </div>
  );
}
