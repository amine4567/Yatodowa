import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

export interface Collection {
  collection_id: string;
  group_id: string | null;
  name: string;
}

@Injectable({ providedIn: 'root' })
export class CollectionsService {
  collectionsUrl: string = 'http://127.0.0.1:4200/api/v1/collections';

  constructor(private http: HttpClient) {}

  getCollections() {
    return this.http.get(this.collectionsUrl);
  }
}
