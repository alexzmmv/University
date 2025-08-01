import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { DestinationsComponent } from './pages/destinations/destinations.component';
import { DestinationDetailComponent } from './pages/destination-detail/destination-detail.component';
import { AddDestinationComponent } from './pages/add-destination/add-destination.component';
import { EditDestinationComponent } from './pages/edit-destination/edit-destination.component';
import { AboutComponent } from './pages/about/about.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'destinations', component: DestinationsComponent, canActivate: [AuthGuard] },
  { path: 'destination/:id', component: DestinationDetailComponent, canActivate: [AuthGuard] },
  { path: 'add-destination', component: AddDestinationComponent, canActivate: [AuthGuard] },
  { path: 'edit-destination/:id', component: EditDestinationComponent, canActivate: [AuthGuard] },
  { path: 'about', component: AboutComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: '' } 
];
