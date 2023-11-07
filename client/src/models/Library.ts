import { CatalogItem } from "./CatalogItem";

export interface Library {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  catalog: CatalogItem[];
}
