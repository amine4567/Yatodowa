import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-current-tasks-list',
  templateUrl: './current-tasks-list.component.html',
  styleUrls: ['./current-tasks-list.component.css'],
})
export class CurrentTasksListComponent implements OnInit {
  tasks: Array<string> = [];
  newTaskVal: string = '';
  tasksUrl: string = 'http://127.0.0.1:5000/api/v1/tasks';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http
      .get(this.tasksUrl, { headers: { 'Access-Control-Allow-Origin': '*' } })
      .subscribe(
        (response: any) => (this.tasks = response.map((obj: any) => obj.text))
      );
  }

  addTask() {
    this.tasks.unshift(this.newTaskVal);
    this.newTaskVal = '';
  }

  deleteTask(index: number) {
    this.tasks.splice(index, 1);
  }
}
