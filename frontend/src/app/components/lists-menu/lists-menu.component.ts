import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {
  CollectionsService,
  Collection,
} from 'app/services/collections.service';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-lists-menu',
  templateUrl: './lists-menu.component.html',
  styleUrls: ['./lists-menu.component.css'],
})
export class ListsMenuComponent implements OnInit {
  @Output() newCollectionSelected = new EventEmitter<Collection>();

  menuItems: MenuItem[] = [];

  constructor(private collectionsService: CollectionsService) {}

  ngOnInit(): void {
    this.collectionsService.getCollections().subscribe((response: any) => {
      this.menuItems = response.collections.map((collection: Collection) => ({
        label: collection.name,
        command: () => this.handleCollectionSelect(collection),
      }));
    });
  }

  handleCollectionSelect(collection: Collection) {
    this.newCollectionSelected.emit(collection);
  }
}
