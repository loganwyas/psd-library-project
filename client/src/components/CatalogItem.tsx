import { CatalogItem } from "@/models/CatalogItem";

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
}

export function ItemFromCatalog(props: ItemProps) {
  let item = props.item;
  return (
    <div className="w-1/2 py-5 mx-auto bg-teal-200 mb-5">
      <p>
        <strong>{item["title"]}</strong> - {item["author"]}
      </p>
      <p>Released: {item["release"]}</p>
      <p>Category: {formatCategory(item["type"])}</p>
    </div>
  );
}
