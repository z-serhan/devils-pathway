import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CareerResultComponent } from './career-result.component';

describe('CareerResultComponent', () => {
  let component: CareerResultComponent;
  let fixture: ComponentFixture<CareerResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CareerResultComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CareerResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
