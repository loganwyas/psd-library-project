"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { User } from "@/models/User";
import { Library } from "@/models/Library";
import { ItemFromCatalog } from "@/components/CatalogItem";
import { CatalogItem } from "@/models/CatalogItem";

const cookies = new Cookies();

export default function Catalog() {
  const [user, setUser] = useState(null as unknown as User);
  const [library, setLibrary] = useState(null as unknown as Library);
  const [loaded, setLoaded] = useState(false);

  const server = "http://127.0.0.1:5001/";
  useEffect(() => {
    let userCookie: User = cookies.get("user");
    if (!userCookie || userCookie.role !== "librarian") {
      redirect("/");
    } else {
      setUser(userCookie);
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
              console.log(response.json());
              return response.json();
            } else {
              throw Error("Failed to get library");
            }
          })
          .then((lib) => setLibrary(lib))
          .catch((error: Error) => console.log(error));
      }
    }
  }, []);

  useEffect(() => {
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
        .then((lib) => setLibrary(lib))
        .catch((error: Error) => console.log(error));
    }
  }, [loaded, user]);

  function saveItem(item: CatalogItem) {
    fetch(server + "edit_library_item?library=" + library.id, {
      method: "POST",
      body: JSON.stringify(item),
      headers: {
        "Content-Type": "application/json",
        Authorization: user.username,
      },
    })
      .then((response) => {
        if (response.status == 200) {
          return response.json();
        }
      })
      .catch((error: Error) => console.log(error));
  }

  return (
    <div className="text-center">
      <h1 className="text-2xl font-bold mb-5 underline">Your Library</h1>
      {library && (
        <div>
          <h2 className="text-xl font-semibold mb-5">{library.name}</h2>
          <h3 className="text-lg font-medium mb-5">
            Located at: {library.latitude} {library.longitude}
          </h3>
          {library.catalog.map((item) => {
            return (
              <ItemFromCatalog item={item} editable saveFunction={saveItem} />
            );
          })}
        </div>
      )}
    </div>
  );
}
