import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  selectedCollectionId: string = '';

  setSelectedCollection(newCollectionId: string) {
    this.selectedCollectionId = newCollectionId;
  }
}
