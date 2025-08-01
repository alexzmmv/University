import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { DestinationsComponent } from './pages/destinations/destinations.component';
import { DestinationDetailComponent } from './pages/destination-detail/destination-detail.component';
import { AddDestinationComponent } from './pages/add-destination/add-destination.component';
import { EditDestinationComponent } from './pages/edit-destination/edit-destination.component';
import { AboutComponent } from './pages/about/about.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'destinations', component: DestinationsComponent },
  { path: 'destination/:id', component: DestinationDetailComponent },
  { path: 'add-destination', component: AddDestinationComponent },
  { path: 'edit-destination/:id', component: EditDestinationComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', redirectTo: '' } 
];
