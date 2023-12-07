// Component for catalog items

import { CatalogItem, LibraryCount } from "@/models/CatalogItem";
import { Library } from "@/models/Library";
import { UserItem } from "@/models/UserItem";
import { useState } from "react";

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

interface ItemProps {
  item: CatalogItem;
  libraries?: { [id: number]: Library };
  userItems?: UserItem[];
  editable?: boolean;
  isUnadded?: boolean;
  saveFunction?: Function;
  deleteFunction?: Function;
}

export function ItemFromCatalog(props: ItemProps) {
  const [editing, setEditing] = useState(false);
  const [item, setItem] = useState({ ...props.item });
  const [editingItem, setEditItem] = useState({ ...props.item });

  function discard() {
    setEditItem({ ...item });
    setEditing(false);
  }

  function save() {
    setItem({ ...editingItem });
    if (props.saveFunction) props.saveFunction({ ...editingItem });
    setEditing(false);
  }

  function deleteItem() {
    if (confirm("You are about to delete this item. Please confirm.")) {
      if (props.deleteFunction) props.deleteFunction(item);
      setEditing(false);
    }
  }

  function checkout(library: number) {
    if (getStatus(library) === "checked_out") {
      if (props.deleteFunction) props.deleteFunction(library, item.id);
    } else {
      if (props.saveFunction) props.saveFunction(library, item.id);
    }
  }

  function getStatus(library: number) {
    if (props.userItems) {
      for (let i = 0; i < props.userItems.length; i++) {
        if (
          props.userItems[i].library === library &&
          props.userItems[i].item === item.id
        ) {
          return props.userItems[i].status;
        }
      }
    }
  }

  function isOneLibraryCheckedOut() {
    if (props.libraries) {
      let libraries = Object.keys(props.libraries);
      for (let i = 0; i < libraries.length; i++) {
        let key = libraries[i];
        let library = props.libraries ? props.libraries[+key] : undefined;
        if (library && getStatus(library.id) === "checked_out") {
          return true;
        }
      }
    }
    return false;
  }

  return (
    <div className="w-1/2 py-5 mx-auto bg-teal-200 mb-5">
      {(props.editable || props.isUnadded) && !editing && (
        <div className="text-right">
          <button
            onClick={() => setEditing(true)}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            {props.editable && "Edit"}
            {props.isUnadded && "+"}
          </button>
        </div>
      )}
      <p>
        <strong>{item["title"]}</strong> - {item["author"]}
      </p>
      <p>Released: {item["release"]}</p>
      <p>Category: {formatCategory(item["type"])}</p>
      {item["count"] && (
        <p>
          <span className="mr-3">Number of this item in stock:</span>
          {!editing && item["count"]}
          {editing && (
            <input
              type="number"
              min="1"
              max="99"
              placeholder={item["count"].toString()}
              onChange={(e) => {
                let temp = editingItem;
                let count = +e.target.value;
                if (count < 1) {
                  count = 1;
                } else if (count > 99) {
                  count = 99;
                }
                e.target.value = count.toString();
                temp["count"] = count;
                setEditItem({ ...temp });
              }}
              id="count"
              className="px-1 w-12"
            />
          )}
        </p>
      )}

      {props.editable && editing && (
        <div className="flex flex-wrap justify-evenly mt-5">
          <button
            onClick={() => discard()}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            Discard
          </button>
          <button
            onClick={() => save()}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            Save
          </button>
          <button
            onClick={() => deleteItem()}
            className="mx-3 px-2 py-1 border border-solid border-red-600 text-red-600"
          >
            Delete
          </button>
        </div>
      )}

      {props.isUnadded && editing && (
        <div className="flex flex-wrap justify-evenly mt-5">
          <button
            onClick={() => discard()}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            Cancel
          </button>
          <div>
            <span className="mr-3">Number of this item in stock:</span>
            <input
              type="number"
              min="1"
              max="99"
              placeholder="1"
              onChange={(e) => {
                let temp = editingItem;
                let count = +e.target.value;
                if (count < 1) {
                  count = 1;
                } else if (count > 99) {
                  count = 99;
                }
                e.target.value = count.toString();
                temp["count"] = count;
                setEditItem({ ...temp });
              }}
              id="count"
              className="px-1 w-12"
            />
          </div>
          <button
            onClick={() => save()}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            Add
          </button>
        </div>
      )}

      {!props.editable &&
        props.libraries &&
        Object.keys(props.libraries).map((key) => {
          let library = props.libraries ? props.libraries[+key] : undefined;
          if (
            library &&
            item.libraryCounts &&
            item.libraryCounts.some((lib) => lib.library === library?.id)
          ) {
            let val = item.libraryCounts.filter(
              (lib) => lib.library === library?.id
            ) as LibraryCount[];
            let count = val.length > 0 ? val[0] : undefined;
            if (
              count &&
              ((count.total > 0 &&
                count.available > 0 &&
                !isOneLibraryCheckedOut()) ||
                getStatus(library.id) === "checked_out")
            ) {
              return (
                <div className="flex flex-wrap justify-around bg-green-200 my-5 p-4">
                  <p>
                    {library.name} - {count.available}/{count.total} Available
                  </p>
                  <button
                    className="mx-3 px-2 py-1 border border-solid border-black"
                    onClick={() => checkout(library?.id as number)}
                  >
                    {getStatus(library?.id) === "checked_out"
                      ? "Return to"
                      : "Checkout from"}{" "}
                    this library
                  </button>
                </div>
              );
            }
          }
          return <div></div>;
        })}
    </div>
  );
}
