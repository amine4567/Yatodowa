import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { TasksService } from 'app/services/tasks.service';

@Component({
  selector: 'app-current-tasks-list',
  templateUrl: './current-tasks-list.component.html',
  styleUrls: ['./current-tasks-list.component.css'],
})
export class CurrentTasksListComponent implements OnInit {
  @Input() collectionId: string = '';

  tasks: Array<any> = [];
  newTaskVal: string = '';

  constructor(private tasksService: TasksService) {}

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges) {
    let selectedCollectionId = changes['collectionId'].currentValue;
    this.tasksService
      .getTasks(selectedCollectionId)
      .subscribe((response: any) => (this.tasks = response.tasks));
  }

  addTask() {
    this.tasks.unshift(this.newTaskVal);
    this.newTaskVal = '';
  }

  deleteTask(index: number) {
    this.tasks.splice(index, 1);
  }
}
