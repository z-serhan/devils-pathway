import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-metacog',
  templateUrl: './metacog.component.html',
  styleUrl: './metacog.component.css'
})
export class MetacogComponent {
  constructor(private router: Router) { }

  goToResources(): void {
    this.router.navigate(['/resources']);
  }
}
