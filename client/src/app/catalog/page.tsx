// Page to search for and display catalog items

"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { CatalogItem } from "@/models/CatalogItem";
import { ItemFromCatalog } from "@/components/CatalogItem";
import { Library } from "@/models/Library";
import { User } from "@/models/User";
import { UserItem } from "@/models/UserItem";
const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null as unknown as User);

  const [search, setSearch] = useState("");
  const [results, setResults] = useState([] as CatalogItem[]);
  const [searchMade, setSearchMade] = useState(false);

  const [libraries, setLibraries] = useState({} as { [id: number]: Library });
  const [gottenLibraries, setGottenLibraries] = useState(false);

  const [userItems, setUserItems] = useState(null as unknown as UserItem[]);
  const [gottenUserItems, setGottenUserItems] = useState(false);

  const server = "http://127.0.0.1:5001/";
  useEffect(() => {
    let userCookie = cookies.get("user");
    if (!userCookie) {
      redirect("/");
    } else {
      setUser(userCookie);
    }
    if (!gottenLibraries) {
      fetch(server + "libraries", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            throw Error("Failed to get libraries");
          }
        })
        .then((libraries) => {
          setGottenLibraries(true);
          setLibraries(libraries);
        })
        .catch((error: Error) => console.log(error));
    }
    setSearch(search.replace(" ", "%20"));
  }, []);

  function sendSearch() {
    setSearchMade(false);
    if (!gottenUserItems && user) {
      fetch(server + "get_user_items?user=" + user.id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            throw Error("Failed to get user items");
          }
        })
        .then((items) => {
          setGottenUserItems(true);
          setUserItems(items);
        })
        .catch((error: Error) => console.log(error));
    }
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
      .then((catalog) => {
        setResults(catalog);
      })
      .catch((error: Error) => console.log(error));
  }

  function inputFilled() {
    return search.trim() === "";
  }

  function checkoutItem(library: number, item: number) {
    fetch(
      server + `checkout_item?library=${library}&user=${user.id}&item=${item}`,
      {
        method: "POST",
        body: JSON.stringify({ item }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => {
        if (response.status == 200) {
          window.location.reload();
        }
      })
      .catch((error: Error) => console.log(error));
  }

  function returnItem(library: number, item: number) {
    fetch(
      server + `return_item?library=${library}&user=${user.id}&item=${item}`,
      {
        method: "POST",
        body: JSON.stringify({ item }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => {
        if (response.status == 200) {
          window.location.reload();
        }
      })
      .catch((error: Error) => console.log(error));
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
      {searchMade &&
        results.length > 0 &&
        results.map((result) => {
          return (
            <ItemFromCatalog
              item={result}
              editable={false}
              userItems={userItems}
              libraries={libraries}
              saveFunction={checkoutItem}
              deleteFunction={returnItem}
            />
          );
        })}
      {searchMade && results.length == 0 && (
        <p>There are no results for your search.</p>
      )}
    </div>
  );
}
