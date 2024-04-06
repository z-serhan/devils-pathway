import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CareerInfoComponent } from './career-info.component';

describe('CareerInfoComponent', () => {
  let component: CareerInfoComponent;
  let fixture: ComponentFixture<CareerInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CareerInfoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CareerInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
