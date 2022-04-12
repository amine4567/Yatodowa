import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-current-tasks-list',
  templateUrl: './current-tasks-list.component.html',
  styleUrls: ['./current-tasks-list.component.css'],
})
export class CurrentTasksListComponent implements OnInit {
  tasks: Array<String> = [
    'Clean the kitchen',
    'Play Elden Ring',
    'Wash the clothes',
  ];
  newTaskVal: String = '';

  constructor() {}

  ngOnInit(): void {}

  addTask() {
    this.tasks.unshift(this.newTaskVal);
    this.newTaskVal = '';
  }

  deleteTask(index: number) {
    this.tasks.splice(index, 1);
  }
}
