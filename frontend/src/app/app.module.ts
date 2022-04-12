import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { CurrentTasksListComponent } from './current-tasks-list/current-tasks-list.component';
import { ListsMenuComponent } from './lists-menu/lists-menu.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    CurrentTasksListComponent,
    ListsMenuComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
