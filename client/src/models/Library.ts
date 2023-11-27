import { CatalogItem } from "./CatalogItem";

export interface Library {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  catalog: CatalogItem[];
}
