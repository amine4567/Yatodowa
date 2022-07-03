import { Component, OnInit } from '@angular/core';
import { CollectionsService } from 'app/services/collections.service';

@Component({
  selector: 'app-lists-menu',
  templateUrl: './lists-menu.component.html',
  styleUrls: ['./lists-menu.component.css'],
})
export class ListsMenuComponent implements OnInit {
  collections: Array<any> = [];

  constructor(private collectionsService: CollectionsService) {}

  ngOnInit(): void {
    this.collectionsService
      .getCollections()
      .subscribe((response: any) => (this.collections = response.collections));
  }
}
