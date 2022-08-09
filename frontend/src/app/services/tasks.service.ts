import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class TasksService {
  constructor(private http: HttpClient) {}

  getTasks(collectionId: string | undefined) {
    let callUrl: string = '';
    if (collectionId) {
      callUrl = `http://127.0.0.1:4200/api/v1/collections/${collectionId}/tasks`;
    } else {
      callUrl = 'http://127.0.0.1:4200/api/v1/tasks';
    }
    return this.http.get(callUrl);
  }
}
