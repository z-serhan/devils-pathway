import { Component } from '@angular/core';
import { CareerService } from '../career.service';
import { ArrayType } from '@angular/compiler';
import { DataService } from '../data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-career-result',
  templateUrl: './career-result.component.html',
  styleUrl: './career-result.component.css'
})
export class CareerResultComponent {

   careers: Array<CombinedCareerInfo> = [];
   careerData: any;
   careerModalOpen: boolean = false;
  
   /*test_careers: CombinedCareerInfo[] = [
    {
      career_name: "Example Career 1",
      career_rationale: "Rationale for career 1",
      career_description: "Description of career 1",
      essential_duties: ["Duty 1", "Duty 2"],
      work_style: ["Style 1", "Style 2"],
      average_salary: 50000,
      related_jobs: [
        { career_title: "Related Job 1-1", career_code: "RJ101" },
        { career_title: "Related Job 1-2", career_code: "RJ102" }
      ],
      classes: [
        { class_name: "Class 1-1", class_code: "C101" },
        { class_name: "Class 1-2", class_code: "C102" }
      ],
      asu_certs: [
        { cert_name: "Certification 1-1", cert_link: "http://example.com/cert1" }
      ]
    },
    // Repeating the structure with variations for additional dummy items
    {
      career_name: "Example Career 2",
      career_rationale: "Rationale for career 2",
      career_description: "Description of career 2",
      essential_duties: ["Duty 3", "Duty 4"],
      work_style: ["Style 3", "Style 4"],
      average_salary: 52000,
      related_jobs: [
        { career_title: "Related Job 2-1", career_code: "RJ201" },
        { career_title: "Related Job 2-2", career_code: "RJ202" }
      ],
      classes: [
        { class_name: "Class 2-1", class_code: "C201" },
        { class_name: "Class 2-2", class_code: "C202" }
      ],
      asu_certs: [
        { cert_name: "Certification 2-1", cert_link: "http://example.com/cert2" }
      ]
    },
    {
      career_name: "Example Career 2",
      career_rationale: "Rationale for career 2",
      career_description: "Description of career 2",
      essential_duties: ["Duty 3", "Duty 4"],
      work_style: ["Style 3", "Style 4"],
      average_salary: 52000,
      related_jobs: [
        { career_title: "Related Job 2-1", career_code: "RJ201" },
        { career_title: "Related Job 2-2", career_code: "RJ202" }
      ],
      classes: [
        { class_name: "Class 2-1", class_code: "C201" },
        { class_name: "Class 2-2", class_code: "C202" }
      ],
      asu_certs: [
        { cert_name: "Certification 2-1", cert_link: "http://example.com/cert2" }
      ]
    },
    {
      career_name: "Example Career 2",
      career_rationale: "Rationale for career 2",
      career_description: "Description of career 2",
      essential_duties: ["Duty 3", "Duty 4"],
      work_style: ["Style 3", "Style 4"],
      average_salary: 52000,
      related_jobs: [
        { career_title: "Related Job 2-1", career_code: "RJ201" },
        { career_title: "Related Job 2-2", career_code: "RJ202" }
      ],
      classes: [
        { class_name: "Class 2-1", class_code: "C201" },
        { class_name: "Class 2-2", class_code: "C202" }
      ],
      asu_certs: [
        { cert_name: "Certification 2-1", cert_link: "http://example.com/cert2" }
      ]
    },
    {
      career_name: "Example Career 2",
      career_rationale: "Rationale for career 2",
      career_description: "Description of career 2",
      essential_duties: ["Duty 3", "Duty 4"],
      work_style: ["Style 3", "Style 4"],
      average_salary: 52000,
      related_jobs: [
        { career_title: "Related Job 2-1", career_code: "RJ201" },
        { career_title: "Related Job 2-2", career_code: "RJ202" }
      ],
      classes: [
        { class_name: "Class 2-1", class_code: "C201" },
        { class_name: "Class 2-2", class_code: "C202" }
      ],
      asu_certs: [
        { cert_name: "Certification 2-1", cert_link: "http://example.com/cert2" }
      ]
    }
  ];*/
  


  constructor(private careerService: CareerService, private dataService: DataService, private router: Router) {}

  ngOnInit() {
    this.careerService.getData().subscribe(data => {
       this.careers = data;
    });
  }

  closeCareerModal(): void {
    this.careerModalOpen = false;
  }

  getCareerData(index: number) {
    let item = this.careers[index];
    this.careerData = {
      career_name: item.career_name,
      career_description: item.career_description,
      essential_duties: item.essential_duties,
      work_style: item.work_style,
      average_salary: item.average_salary,
      related_jobs: item.related_jobs,
    };
    this.careerModalOpen = true;
  }

  goToMeta() {
    this.router.navigate(['/metacog']);
  }
}

interface CareerData {
  career_name: string;
  career_description: string;
  essential_duties: string[];
  work_style: string[];
  average_salary: number;
  related_jobs: { career_title: string; career_code: string }[];
}


interface CombinedCareerInfo {
  career_name: string;
  career_rationale: string;
  career_description: string;
  essential_duties: string[];
  work_style: string[];
  average_salary: number;
  related_jobs: { career_title: string; career_code: string }[];
  classes: { class_name: string; class_code: string }[];
  asu_certs: { cert_name: string; cert_link: string }[];
}

