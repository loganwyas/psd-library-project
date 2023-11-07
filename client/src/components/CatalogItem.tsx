import { CatalogItem } from "@/models/CatalogItem";
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
  editable?: boolean;
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

  return (
    <div className="w-1/2 py-5 mx-auto bg-teal-200 mb-5">
      {props.editable && !editing && (
        <div className="text-right">
          <button
            onClick={() => setEditing(true)}
            className="mx-3 px-2 py-1 border border-solid border-black"
          >
            Edit
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
    </div>
  );
}
