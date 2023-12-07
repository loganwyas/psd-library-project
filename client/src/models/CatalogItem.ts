// Type for catalog items

export interface CatalogItem {
  id: number;
  title: string;
  author: string;
  release: number;
  type: string;
  count?: number;
  libraryCounts?: LibraryCount[];
}

export interface LibraryCount {
  library: number;
  total: number;
  available: number;
}
