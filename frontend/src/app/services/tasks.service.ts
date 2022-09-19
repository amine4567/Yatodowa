import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

export interface Task{
  text: string;
  collection_id: string;
}

@Injectable({ providedIn: 'root' })
export class TasksService {
  constructor(private http: HttpClient) {}

  getTasks(collectionId: string | undefined) {
    let callUrl: string = '';
    if (collectionId) {
      callUrl = `/api/v1/collections/${collectionId}/tasks`;
    } else {
      callUrl = '/api/v1/tasks';
    }
    return this.http.get(callUrl);
  }

  addTask(text:string, collection_id: string) {
    return this.http.post(
      '/api/v1/tasks', 
      {"text": text, "collection_id": collection_id}
    );
  }
}
