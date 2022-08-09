import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';

import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { DataViewModule } from 'primeng/dataview';
import { PanelMenuModule } from 'primeng/panelmenu';

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
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    InputTextModule,
    ButtonModule,
    DataViewModule,
    PanelMenuModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
