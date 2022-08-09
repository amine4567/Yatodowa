import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { TasksService } from 'app/services/tasks.service';
import { Collection } from 'app/services/collections.service';

@Component({
  selector: 'app-current-tasks-list',
  templateUrl: './current-tasks-list.component.html',
  styleUrls: ['./current-tasks-list.component.css'],
})
export class CurrentTasksListComponent implements OnInit {
  @Input() selectedCollection!: Collection;

  tasks: Array<any> = [];
  newTaskVal: string = '';

  checked: boolean = true;

  constructor(private tasksService: TasksService) {}

  ngOnInit(): void {
    this.tasksService
      .getTasks(undefined)
      .subscribe((response: any) => (this.tasks = response.tasks));
  }

  ngOnChanges(changes: SimpleChanges) {
    let selectedCollectionId =
      changes['selectedCollection'].currentValue.collection_id;
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
