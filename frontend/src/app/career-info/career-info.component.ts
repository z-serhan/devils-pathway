import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-career-info',
  templateUrl: './career-info.component.html',
  styleUrl: './career-info.component.css'
})
export class CareerInfoComponent {

  @Input() showModal: boolean = false;
  @Input() careerData: any;
  @Output() closeModalEvent = new EventEmitter<void>();



  constructor() { }
  ngOnInit(): void {
  }

  closeModal(): void {
    this.showModal = false;
    this.closeModalEvent.emit();
  }
}
