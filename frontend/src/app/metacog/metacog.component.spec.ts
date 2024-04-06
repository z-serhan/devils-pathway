import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetacogComponent } from './metacog.component';

describe('MetacogComponent', () => {
  let component: MetacogComponent;
  let fixture: ComponentFixture<MetacogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MetacogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MetacogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
