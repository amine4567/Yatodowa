import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CollectionsService } from 'app/services/collections.service';

@Component({
  selector: 'app-lists-menu',
  templateUrl: './lists-menu.component.html',
  styleUrls: ['./lists-menu.component.css'],
})
export class ListsMenuComponent implements OnInit {
  @Output() newCollectionSelected = new EventEmitter<string>();

  collections: Array<any> = [];

  constructor(private collectionsService: CollectionsService) {}

  ngOnInit(): void {
    this.collectionsService
      .getCollections()
      .subscribe((response: any) => (this.collections = response.collections));
  }

  handleCollectionSelect(collectionId: string) {
    this.newCollectionSelected.emit(collectionId);
  }
}
