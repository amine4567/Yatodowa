import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class TasksService {
  tasksUrl: string = 'http://127.0.0.1:4200/api/v1/tasks';

  constructor(private http: HttpClient) {}

  getTasks() {
    return this.http.get(this.tasksUrl);
  }
}
