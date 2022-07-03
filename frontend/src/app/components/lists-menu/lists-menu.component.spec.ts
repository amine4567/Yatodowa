import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListsMenuComponent } from './lists-menu.component';

describe('ListsMenuComponent', () => {
  let component: ListsMenuComponent;
  let fixture: ComponentFixture<ListsMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListsMenuComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListsMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
