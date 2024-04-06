import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CareerService {

  private dataSource = new BehaviorSubject<any>(null);

  sendData(data: any) {
    this.dataSource.next(data);
  }

  getData(): Observable<any> {
    return this.dataSource.asObservable();
  }
}
