import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { CurrentTasksListComponent } from './components/current-tasks-list/current-tasks-list.component';
import { ListsMenuComponent } from './components/lists-menu/lists-menu.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    CurrentTasksListComponent,
    ListsMenuComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
