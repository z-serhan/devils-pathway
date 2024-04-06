import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule here
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { TypeaheadModule } from 'ngx-bootstrap/typeahead';



import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { StudentInfoComponent } from './student-info/student-info.component';
import { CareerInfoComponent } from './career-info/career-info.component';
import { CareerResultComponent } from './career-result/career-result.component';
import { ResourcesComponent } from './resources/resources.component';
import { MetacogComponent } from './metacog/metacog.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    StudentInfoComponent,
    CareerInfoComponent,
    CareerResultComponent,
    ResourcesComponent,
    MetacogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    TypeaheadModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
