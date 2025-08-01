import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, ActivatedRoute } from '@angular/router';
import { DestinationService } from '../../services/destination.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  destinations: any[] = [];
  countries: any[] = [];
  costRange = { min_cost: 0, max_cost: 0 };
  pagination = {
    currentPage: 1,
    totalPages: 1,
    totalItems: 0
  };
  totalDestinations: number = 0; // New property for destinations-num endpoint
  loading = true;
  error: string | null = null;
  success: string | null = null;

  constructor(
    private destinationService: DestinationService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    // Get query parameters (success/error messages)
    this.route.queryParams.subscribe(params => {
      if (params['success']) {
        this.success = params['success'];
      }
      if (params['error']) {
        this.error = params['error'];
      }
    });

    this.loadData();
  }

  loadData(): void {
    this.loadDestinations();
    this.loadCountries();
    this.loadCostRange();
    this.loadTotalDestinations(); // New method to load total from destinations-num endpoint
  }

  loadDestinations(): void {
    this.loading = true;
    this.destinationService.getDestinations(
      this.pagination.currentPage, 
      3,  // Limit to 4 destinations on home page
      {}  // No filters on home page
    ).subscribe({
      next: (data) => {
        this.destinations = data.destinations || [];
        if (data.pagination) {
          this.pagination.currentPage = data.pagination.current_page;
          this.pagination.totalPages = data.pagination.total_pages;
          this.pagination.totalItems = data.pagination.total_items;
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
      },
      error: (err) => {
        console.error('Error loading cost range:', err);
      }
    });
  }

  // New method to load total destinations from the destinations-num endpoint
  loadTotalDestinations(): void {
    this.destinationService.getDestinationsCount().subscribe({
      next: (data) => {
        if (data && data.status === 'success') {
          this.totalDestinations = data.total;
        }
      },
      error: (err) => {
        console.error('Error loading total destinations count:', err);
      }
    });
  }

  changePage(page: number): void {
    if (page < 1 || page > this.pagination.totalPages) {
      return;
    }
    this.pagination.currentPage = page;
    this.loadDestinations();
  }
}
