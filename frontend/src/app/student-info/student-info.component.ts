import { Component } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { Router } from '@angular/router';
import { DataService } from '../data.service';
import { CareerService } from '../career.service';
import { last } from 'rxjs';



@Component({
  selector: 'app-student-info',
  templateUrl: './student-info.component.html',
  styleUrls: ['./student-info.component.css'],
  animations: [
    trigger('stepTransition', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('500ms ease-out', style({ transform: 'translateX(0)', opacity: 1 })),
      ]),
      transition(':leave', [
        animate('1ms', style({ transform: 'translateX(-100%)', opacity: 0 })),
      ])
    ])
  ]
})

export class StudentInfoComponent {
  currentStep = 1;
  userDetails = { major: '', interests: '' };
  majors = [];
  // Create an object that fits the StudentInfo interface
  studentInfo: StudentInfo = {
    major: "",
    interests: [],
    skills: []
  };
  // Empty instance of Chapter
  currentChapter: Chapter = {
    chapterNumber: 0,
    chapterTitle: "",
    chapterDescription: "",
    chapterOptions: []
  }; 
  selectedOption: number = 0; 
  GPTMessages: Array<ChatGPTMessage> = []
  skillChips: string[] = [];
  interestChips: string[] = [];
  interestsInputValue: string = '';
  skillsInputValue: string = '';
  step_number = 0;
  isLoading = false;
  personalities: Array<PersonalityType> = []
  values: Array<WorkValue> = []
  jpegFiles: Array<string> = []

  //dummy data

  /*personalities: Array<PersonalityType>= [
    {
      "name": "Innovator",
      "description": "Thrives on creativity and the implementation of new ideas."
    },
    {
      "name": "Analyzer",
      "description": "Prefers working with data and analytical processes to make informed decisions."
    },
    {
      "name": "Communicator",
      "description": "Excels in expressing ideas and engaging effectively with people."
    }
  ]
  values: Array<WorkValue>= [
    {
      "name": "Autonomy",
      "description": "Values the freedom to make decisions and prioritize work independently."
    },
    {
      "name": "Collaboration",
      "description": "Appreciates a team-oriented environment with shared goals and teamwork."
    },
    {
      "name": "Innovation",
      "description": "Places importance on a culture that encourages creativity and new ideas."
    }
  ] */




 
  constructor(
    private router: Router,
    private dataService: DataService,
    private careerService: CareerService
  ){}

  ngOnInit(): void {
    this.loading();
    this.dataService.getASUMajors().subscribe((res:any)=>{
      this.stopLoading();
      this.majors = res;
    })
  }

  getFirstMessage() {
    let interest_list = this.studentInfo.interests.join(", ");
    this.loading();
    this.dataService.chatRIASEC({"step_number":this.step_number, "messages":[], "interests":interest_list}).subscribe((res:any)=>{
      this.stopLoading();
      this.GPTMessages = res;
      if (this.GPTMessages && this.GPTMessages.length > 0) {
        const lastMessage = this.GPTMessages[this.GPTMessages.length - 1];
        try {
          // Parsing the stringified currentChapter from the last message's content
          this.currentChapter = JSON.parse(lastMessage.content);
          this.goToNextStep();
        } catch (error) {
          console.error('Error parsing currentChapter:', error);
          // Handle the error (e.g., set currentChapter to a default value or show an error message)
        }
      }
    });
  }

  getNewChapter() {
    this.loading();
    this.step_number ++;
    this.GPTMessages.push({
      content: this.selectedOption.toString(),
      role: "user"
    });
    this.dataService.chatRIASEC({"step_number":this.step_number, "messages":this.GPTMessages}).subscribe((res:any)=>{
      this.GPTMessages = res;
      if (this.GPTMessages && this.GPTMessages.length > 0) {
        const lastMessage = this.GPTMessages[this.GPTMessages.length - 1];
        console.log(this.step_number);
        try {
          // Parsing the stringified currentChapter from the last message's content
          if(this.step_number == 8) {
            this.personalities = JSON.parse(lastMessage.content).personalities;
            this.values = JSON.parse(lastMessage.content).work_values;
            this.jpegFiles = this.mapPersonalityTypesToJpeg(this.personalities)
          }
          else {
            this.currentChapter = JSON.parse(lastMessage.content);
            this.selectedOption = 0; 
          }
          this.stopLoading();
          this.goToNextStep();
        } catch (error) {
          console.error('Error parsing currentChapter:', error);
          // Handle the error (e.g., set currentChapter to a default value or show an error message)
        }
      }
    });
  }

  getCareers() {
    this.loading();
    let student_profile = this.createStudentProfile(this.studentInfo, this.personalities)
    this.dataService.chatCareer(student_profile).subscribe((res:any)=>{
      this.careerService.sendData(res)
      this.stopLoading();
      this.router.navigate(['/career-result']);
    });
  }

  // Function to create the desired object
  createStudentProfile(info: StudentInfo, personalities: PersonalityType[]): any {
    const profile = {
      student_major: info.major,
      student_interests: info.interests.join(", "), 
      student_skills: info.skills.join(", "), // Converting array to comma-separated string
      student_riasec: personalities.map(p => p.name).join(", ")  // Converting names to comma-separated string
    };
    return profile;
  }

  goToNextStep(): void {
    this.currentStep++;
  }

  onSubmit(): void {
    console.log(this.userDetails);
  }

  addSkillChip(): void {
    const value = this.skillsInputValue.trim();
    if (value) {
      this.skillChips.push(value);
      this.studentInfo.skills.push(value); // Add to interests list as well
      this.skillsInputValue = '';
    }
    console.log(this.studentInfo);
  }

  removeSkillChip(index: number): void {
    const removedChip = this.skillChips.splice(index, 1);
    this.studentInfo.skills = this.studentInfo.skills.filter(skill => skill !== removedChip[0]);
  }

  addInterestChip(): void {
    const value = this.interestsInputValue.trim();
    if (value) {
      this.interestChips.push(value);
      this.studentInfo.interests.push(value); // Add to interests list as well
      this.interestsInputValue = '';
    }
    console.log(this.studentInfo);
  }

  removeInterestChip(index: number): void {
    const removedChip = this.interestChips.splice(index, 1);
    this.studentInfo.interests = this.studentInfo.interests.filter(interest => interest !== removedChip[0]);
  }

  loading() {
    this.isLoading = true;
  }
  stopLoading() {
    this.isLoading = false;
  }


   mapPersonalityTypesToJpeg(personalityTypes: PersonalityType[]): string[] {
    const codeToJpegMap: { [key: string]: string } = {
      Artistic: "assets/A.jpg",
      Realistic: "assets/R.jpg",
      Investigative: "assets/I.jpg",
      Social: "assets/S.jpg",
      Enterprising: "assets/E.jpg",
      Conventional: "assets/C.jpg"
    };
  
    // Map each personality type to its corresponding JPEG based on the RIASEC code in its name
    const jpegFiles: string[] = personalityTypes.reduce((acc: string[], currentType: PersonalityType) => {
      // Check each code in the map to see if it's included in the personality type name
      Object.entries(codeToJpegMap).forEach(([key, value]) => {
        if (currentType.name.includes(key)) {
          acc.push(value);
        }
      });
      return acc;
    }, []);
  
    return jpegFiles;
  }
}
interface StudentInfo {
  major: string;
  interests: string[];
  skills: string[];
}

interface ChatGPTMessage {
  role: string;
  content: string;
}

export interface Chapter {
  chapterNumber: number;
  chapterTitle: string;
  chapterDescription: string;
  chapterOptions: Array<ChapterOptions>;
}

interface ChapterOptions {
  optionNumber: number;
  optionDescription: string;
}

interface PersonalityType {
  name: string;
  description: string;
}

interface WorkValue {
  name: string;
  description: string;
}