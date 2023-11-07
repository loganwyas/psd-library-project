"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { User } from "@/models/User";
import { Library } from "@/models/Library";
import { ItemFromCatalog } from "@/components/CatalogItem";
import { CatalogItem } from "@/models/CatalogItem";

const cookies = new Cookies();

export default function LibraryItemAdd() {
  const [user, setUser] = useState(null as unknown as User);
  const [library, setLibrary] = useState(null as unknown as Library);
  const [unaddedItems, setUnaddedItems] = useState(
    [] as unknown as CatalogItem[]
  );
  const [loaded, setLoaded] = useState(false);

  const server = "http://127.0.0.1:5001/";

  function getLibrary() {
    if (!loaded && user) {
      setLoaded(true);
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
            throw Error("Failed to get library");
          }
        })
        .then((lib: Library) => {
          setLibrary(lib);
          return lib;
        })
        .then((lib) => {
          fetch(server + "unadded_library_items?library=" + lib.id, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          })
            .then((response) => {
              if (response.status == 200) {
                return response.json();
              } else {
                throw Error("Failed to get unadded library items");
              }
            })
            .then((items: CatalogItem[]) => setUnaddedItems(items))
            .catch((error: Error) => console.log(error));
        })
        .catch((error: Error) => console.log(error));
    }
  }

  useEffect(() => {
    let userCookie: User = cookies.get("user");
    if (!userCookie || userCookie.role !== "librarian") {
      redirect("/");
    } else {
      setUser(userCookie);
      getLibrary();
    }
  }, []);

  useEffect(() => {
    getLibrary();
  }, [loaded, user]);

  function addItem(item: CatalogItem) {
    fetch(server + "add_library_item?library=" + library.id, {
      method: "POST",
      body: JSON.stringify(item),
      headers: {
        "Content-Type": "application/json",
        Authorization: user.username,
      },
    })
      .then((response) => {
        if (response.status == 200) {
          window.location.reload();
        }
      })
      .catch((error: Error) => console.log(error));
  }

  return (
    <div className="text-center">
      <h1 className="text-2xl font-bold mb-5 underline">
        Add Items to Library
      </h1>
      {library && unaddedItems && (
        <div>
          {unaddedItems.map((item) => {
            return (
              <ItemFromCatalog item={item} isUnadded saveFunction={addItem} />
            );
          })}
        </div>
      )}
    </div>
  );
}
