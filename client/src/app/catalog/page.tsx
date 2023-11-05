"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { CatalogItem } from "@/models/CatalogItem";
import { ItemFromCatalog } from "@/components/CatalogItem";
const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null);
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([] as CatalogItem[]);
  const [searchMade, setSearchMade] = useState(false);

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
        setSearchMade(true);
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

  return (
    <div className="text-center">
      <h1 className="text-2xl font-bold mb-5">Library Catalog</h1>
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
          return <ItemFromCatalog item={result} />;
        })}
      {searchMade && results.length == 0 && (
        <p>There are no results for your search.</p>
      )}
    </div>
  );
}
