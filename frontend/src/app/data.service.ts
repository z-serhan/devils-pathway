import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { ActivatedRouteSnapshot, Resolve } from '@angular/router';

@Injectable({
  providedIn: 'root'
})

export class DataService {

  constructor(private api: ApiService) { }
    
  private backend_url = 'http://localhost:5000';
  private onet_url = 'http://localhost:5000/onet';

  chatWithGPT() {
    return this.api.get(this.backend_url + '/chat');
  }

  getASUMajors() {
    return this.api.get(this.backend_url + '/majors');
  }

  getCareerByID(careerID:string){
    return this.api.get(this.onet_url + '/careers/' + careerID +'/report')
  }

  chatRIASEC(chat_details:any){
    return this.api.post(this.backend_url + '/gpt-riasec', chat_details)
  }

  chatCareer(student_info:any){
    return this.api.post(this.backend_url + '/gpt-career', student_info)
  }
}
