import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, ActivatedRoute, Router } from '@angular/router';
import { DestinationService } from '../../services/destination.service';

@Component({
  selector: 'app-edit-destination',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './edit-destination.component.html',
  styleUrl: './edit-destination.component.css'
})
export class EditDestinationComponent implements OnInit {
  destination: any = {
    id: 0,
    name: '',
    country_name: '',
    description: '',
    cost_per_day: 0,
    cost: 0,
    tourist_targets: '',
    attractions: ''
  };
  
  originalDestination: any = {};
  countries: any[] = [];
  loading = true;
  saving = false;
  error: string | null = null;
  formSubmitted = false;

  constructor(
    private destinationService: DestinationService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = +params['id'];
      this.loadDestination(id);
    });
    this.loadCountries();
  }

  loadDestination(id: number): void {
    this.loading = true;
    this.destinationService.getDestination(id).subscribe({
      next: (data) => {
        if (data) {
          this.destination = data;
          
          // Ensure we have both cost_per_day and cost properties synchronized
          if (this.destination.cost_per_day && !this.destination.cost) {
            this.destination.cost = this.destination.cost_per_day;
          } else if (this.destination.cost && !this.destination.cost_per_day) {
            this.destination.cost_per_day = this.destination.cost;
          }
          
          // Ensure we have both tourist_targets and attractions properties synchronized
          if (this.destination.tourist_targets && !this.destination.attractions) {
            this.destination.attractions = this.destination.tourist_targets;
          } else if (this.destination.attractions && !this.destination.tourist_targets) {
            this.destination.tourist_targets = this.destination.attractions;
          }
          
          // Make a copy of the original data for comparison
          this.originalDestination = {...this.destination};
        }
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Error loading destination. It may have been deleted or does not exist.';
        this.loading = false;
        console.error('Error fetching destination:', error);
      }
    });
  }

  loadCountries(): void {
    this.destinationService.getCountries().subscribe({
      next: (data) => {
        this.countries = data.countries || [];
      },
      error: (err) => {
        console.error('Error loading countries:', err);
      }
    });
  }

  onSubmit(): void {
    this.formSubmitted = true;
    
    // Form validation
    if (!this.validateForm()) {
      return;
    }
    
    this.saving = true;
    this.error = null;
    
    // Ensure cost and cost_per_day are synchronized
    this.destination.cost_per_day = this.destination.cost;
    
    this.destinationService.updateDestination(this.destination.id, this.destination).subscribe({
      next: (response) => {
        this.saving = false;
        // Navigate back to the destination detail page
        this.router.navigate(['/destination', this.destination.id], { 
          queryParams: { 
            success: 'Destination successfully updated!' 
          }
        });
      },
      error: (err) => {
        this.saving = false;
        this.error = 'Failed to update destination. Please try again.';
        console.error('Error updating destination:', err);
      }
    });
  }

  validateForm(): boolean {
    // Check required fields
    if (!this.destination.name.trim()) {
      this.error = 'Destination name is required.';
      return false;
    }
    
    if (!this.destination.country_name.trim()) {
      this.error = 'Country name is required.';
      return false;
    }
    
    if (!this.destination.description.trim()) {
      this.error = 'Description is required.';
      return false;
    }
    
    if (this.destination.cost <= 0) {
      this.error = 'Cost must be greater than zero.';
      return false;
    }
    
    // All validations passed
    return true;
  }

  // Helper to check if the form has changes
  hasChanges(): boolean {
    return JSON.stringify(this.destination) !== JSON.stringify(this.originalDestination);
  }
}
