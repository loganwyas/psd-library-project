"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null);
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

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
        } else {
          throw Error("Failed to get catalog");
        }
      })
      .then((catalog) => setResults(catalog))
      .catch((error: Error) => console.log(error));
  }

  function inputFilled() {
    return search.trim() === "";
  }

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
          "mx-3 mb-5 px-2 py-1 border border-solid border-black " +
          (inputFilled() ? "text-gray-400 border-gray-400" : "")
        }
        disabled={inputFilled()}
      >
        Search
      </button>
      {results.length > 0 &&
        results.map((result) => {
          return (
            <div className="w-1/2 py-5 mx-auto bg-teal-200 mb-5">
              <p>
                <strong>{result["title"]}</strong> - {result["author"]}
              </p>
              <p>Released: {result["release"]}</p>
              <p>Category: {formatCategory(result["type"])}</p>
            </div>
          );
        })}
      {results.length == 0 && <p>There are no results for your search.</p>}
    </div>
  );
}
