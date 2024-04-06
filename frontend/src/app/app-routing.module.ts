import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { StudentInfoComponent } from './student-info/student-info.component';
import { CareerInfoComponent } from './career-info/career-info.component';
import { CareerResultComponent } from './career-result/career-result.component';
import { ResourcesComponent } from './resources/resources.component';
import { MetacogComponent } from './metacog/metacog.component';

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
    title: 'Home'
  },
  {
    path: 'student-info',
    component: StudentInfoComponent,
    title: 'Student Info'
  },
  {
    path: 'career-info',
    component: CareerInfoComponent,
    title: 'Career Info'
  },
  {
    path: 'career-result',
    component: CareerResultComponent,
    title: 'Career Result'
  },
  {
    path: 'resources',
    component: ResourcesComponent,
    title: 'Resources'
  },
  {
    path: 'metacog',
    component: MetacogComponent,
    title: 'Last step'
  },
  {
    path: '',
    component: HomeComponent,
    title: 'Home'
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
