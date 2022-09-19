import { Component, OnInit, Input } from '@angular/core';
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

  ngOnChanges() {
    this.refreshTasks()
  }

  refreshTasks() {
    this.tasksService.getTasks(this.selectedCollection.collection_id).subscribe(
      (response: any) => (this.tasks = response.tasks)
    );
  }

  addTask() {
    this.tasksService.addTask(
      this.newTaskVal, 
      this.selectedCollection.collection_id
    ).subscribe(() => this.refreshTasks());
    this.newTaskVal = '';
  }

  deleteTask(index: number) {
    this.tasks.splice(index, 1);
  }
}
