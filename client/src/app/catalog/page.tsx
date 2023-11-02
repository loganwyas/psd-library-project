"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null);
  const [search, setSearch] = useState("");

  const server = "http://127.0.0.1:5001/";
  useEffect(() => {
    let userCookie = cookies.get("user");
    if (!userCookie) {
      redirect("/");
    } else {
      setUser(userCookie);
    }
    setSearch(search.replace(" ", "%20"));
  }, []);

  function sendSearch() {
    fetch(server + "catalog?search=" + search, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.status == 200) {
          return response.json();
        }
      })
      .then((response) => console.log(response))
      .catch((error: Error) => console.log(error));
  }

  function inputFilled() {
    return search.trim() === "";
  }

  return (
    <div className="text-center">
      <h1>Library Catalog</h1>
      <label htmlFor="search">Search: </label>
      <input
        onChange={(e) => setSearch(e.target.value)}
        id="search"
        className="px-1"
      />
      <button
        onClick={() => sendSearch()}
        className={
          "mr-3 p-2 border border-solid border-black " +
          (inputFilled() ? "text-gray-400 border-gray-400" : "")
        }
        disabled={inputFilled()}
      >
        Search
      </button>
    </div>
  );
}
