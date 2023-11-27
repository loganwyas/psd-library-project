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
  }, []);

  useEffect(() => {
    if (!gottenUserItems && user) {
      setSearchMade(false);
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
          fetch(server + "catalog", {
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
            .then((catalog) => {
              let newCatalog = [] as CatalogItem[];
              for (let i = 0; i < items.length; i++) {
                let item = items[i] as UserItem;
                for (let x = 0; x < catalog.length; x++) {
                  let catalogItem = catalog[x] as CatalogItem;
                  if (item.item === catalogItem.id) {
                    newCatalog.push(catalogItem);
                  }
                }
              }
              setResults(newCatalog);
              setSearchMade(true);
            })
            .catch((error: Error) => console.log(error));
        })
        .catch((error: Error) => console.log(error));
    }
  }, [user]);

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
      <h1 className="text-2xl font-bold mb-5">My Items</h1>
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
      {searchMade && results.length == 0 && <p>You do not have any items.</p>}
    </div>
  );
}
