import { Component } from '@angular/core';
import { Collection } from 'app/services/collections.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  selectedCollection!: Collection;

  ngOnInit(): void {}

  setSelectedCollection(newCollection: Collection) {
    this.selectedCollection = newCollection;
  }
}
