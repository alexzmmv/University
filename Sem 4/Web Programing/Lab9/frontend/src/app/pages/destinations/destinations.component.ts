import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { DestinationService } from '../../services/destination.service';

@Component({
  selector: 'app-destinations',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './destinations.component.html',
  styleUrl: './destinations.component.css'
})
export class DestinationsComponent implements OnInit {
  destinations: any[] = [];
  countries: any[] = [];
  costRange = { min_cost: 0, max_cost: 0 };
  
  filters = {
    search: '',
    min_cost: 0,
    max_cost: 10000000, 
    countries: [] as number[]
  };
  
  pagination = {
    currentPage: 1,
    totalPages: 1,
    totalItems: 0
  };
  
  loading = true;
  error: string | null = null;

  constructor(private destinationService: DestinationService) { }

  ngOnInit(): void {
    this.loadCostRange();
    this.loadCountries();
    this.loadDestinations();
  }


  loadDestinations(): void {
    this.loading = true;
    this.error = null;
    
    // Log the filters being applied
    console.log('Applying filters:', JSON.stringify(this.filters));
    
    this.destinationService.getDestinations(
      this.pagination.currentPage, 
      4,
      this.filters
    ).subscribe({
      next: (data) => {
        console.log('API response:', data);
        this.destinations = data.destinations || [];
        if (data.pagination) {
          this.pagination.currentPage = data.pagination.currentPage;
          this.pagination.totalPages = data.pagination.totalPages;
          this.pagination.totalItems = data.pagination.totalItems;
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load destinations. Please try again.';
        this.loading = false;
        console.error('Error loading destinations:', err);
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

  loadCostRange(): void {
    this.destinationService.getCostRange().subscribe({
      next: (range) => {
        this.costRange = range;
        // Set initial filter values based on the actual range
        this.filters.min_cost = this.costRange.min_cost;
        this.filters.max_cost = this.costRange.max_cost;
      },
      error: (err) => {
        console.error('Error loading cost range:', err);
      }
    });
  }

  applyFilters(): void {
    this.pagination.currentPage = 1; // Reset to first page when applying filters
    this.loadDestinations();
  }

  resetFilters(): void {
    this.filters = {
      search: '',
      min_cost: this.costRange.min_cost,
      max_cost: this.costRange.max_cost,
      countries: []
    };
    this.pagination.currentPage = 1;
    this.loadDestinations();
  }

  changePage(page: number): void {
    if (page < 1 || page > this.pagination.totalPages) {
      return;
    }
    this.pagination.currentPage = page;
    this.loadDestinations();
  }

  toggleCountryFilter(countryId: number): void {
    console.log('Toggling country filter for ID:', countryId);
    const index = this.filters.countries.indexOf(countryId);
    if (index === -1) {
      this.filters.countries.push(countryId);
      console.log('Added country ID to filters:', countryId);
    } else {
      this.filters.countries.splice(index, 1);
      console.log('Removed country ID from filters:', countryId);
    }
    console.log('Current country filters:', this.filters.countries);
    this.applyFilters(); // Automatically apply filters when toggling a country
  }

  countryIsSelected(countryId: number): boolean {
    return this.filters.countries.includes(countryId);
  }

  onMinCostChange(event: Event): void {
    const value = +(event.target as HTMLInputElement).value;
    
    // Ensure min_cost doesn't exceed max_cost
    if (value > this.filters.max_cost) {
      this.filters.min_cost = this.filters.max_cost;
    }
  }

  onMaxCostChange(event: Event): void {
    const value = +(event.target as HTMLInputElement).value;
    
    if (value < this.filters.min_cost) {
      this.filters.max_cost = this.filters.min_cost;
    }
  }

  getSelectedCountryNames(): string[] {
    return this.countries
      .filter(country => this.filters.countries.includes(country.id))
      .map(country => country.name);
  }

  removeCountryByName(countryName: string): void {
    const country = this.countries.find(c => c.name === countryName);
    if (country) {
      const index = this.filters.countries.indexOf(country.id);
      if (index !== -1) {
        this.filters.countries.splice(index, 1);
        this.applyFilters(); // Automatically apply filters when removing a country
      }
    }
  }
}
