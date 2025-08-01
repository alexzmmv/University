import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { DestinationService } from '../../services/destination.service';

@Component({
  selector: 'app-add-destination',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './add-destination.component.html',
  styleUrl: './add-destination.component.css'
})
export class AddDestinationComponent implements OnInit {
  newDestination = {
    name: '',
    country_name: '',
    description: '',
    cost_per_day: 0,
    tourist_targets: '',
    cost: 0,
    attractions: ''
  };
  
  countries: any[] = [];
  loading = false;
  error: string | null = null;
  success: string | null = null;
  formSubmitted = false;

  constructor(
    private destinationService: DestinationService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadCountries();
  }

  loadCountries(): void {
    this.destinationService.getCountries().subscribe({
      next: (data) => {
        this.countries = data.countries || [];
      },
      error: (err) => {
        console.error('Error loading countries:', err);
        this.error = 'Failed to load countries. Please refresh and try again.';
      }
    });
  }

  onSubmit(): void {
    this.formSubmitted = true;
    
    if (!this.validateForm()) {
      return;
    }
    
    this.loading = true;
    this.error = null;
    
    this.newDestination.cost = this.newDestination.cost_per_day;
    this.newDestination.attractions = this.newDestination.tourist_targets;
    
    this.destinationService.addDestination(this.newDestination).subscribe({
      next: (response) => {
        this.loading = false;
        this.success = 'Destination added successfully!';
        this.resetForm();
        setTimeout(() => {
          this.router.navigate(['/destination', response.destination.id], { 
            queryParams: { 
              success: 'Destination successfully created!' 
            }
          });
        }, 1500);
      },
      error: (err) => {
        this.loading = false;
        this.error = 'Failed to create destination. Please try again.';
        console.error('Error creating destination:', err);
      }
    });
  }

  resetForm(): void {
    this.newDestination = {
      name: '',
      country_name: '',
      description: '',
      cost_per_day: 0,
      tourist_targets: '',
      cost: 0,
      attractions: ''
    };
    this.formSubmitted = false;
  }

  validateForm(): boolean {
    if (!this.newDestination.name.trim()) {
      this.error = 'Destination name is required.';
      return false;
    }
    
    if (!this.newDestination.country_name.trim()) {
      this.error = 'Country name is required.';
      return false;
    }
    
    if (!this.newDestination.description.trim()) {
      this.error = 'Description is required.';
      return false;
    }
    
    if (this.newDestination.cost_per_day <= 0) {
      this.error = 'Cost per day must be a positive number.';
      return false;
    }
    
    return true;
  }
}
