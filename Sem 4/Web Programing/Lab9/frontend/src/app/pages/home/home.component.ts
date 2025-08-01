import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, ActivatedRoute } from '@angular/router';
import { DestinationService } from '../../services/destination.service';
import { AuthService } from '../../services/auth.service';

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
    private authService: AuthService,
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
    if (this.isLoggedIn()) {
      this.loadDestinations();
      this.loadCountries();
      this.loadCostRange();
      this.loadTotalDestinations();
    } else {
      this.loading = false;
    }
  }

  isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  loadDestinations(): void {
    this.loading = true;
    this.destinationService.getDestinations(
      this.pagination.currentPage, 
      3,  // Limit to 3 destinations on home page
      {}  // No filters on home page
    ).subscribe({
      next: (data) => {
        // Adapt to .NET backend response format
        this.destinations = data.data || data.destinations || [];
        
        if (data.pagination) {
          this.pagination.currentPage = data.pagination.currentPage;
          this.pagination.totalPages = data.pagination.totalPages;
          this.pagination.totalItems = data.pagination.totalItems;
        } else if (data.meta) {
          // For .NET backend
          this.pagination.currentPage = data.meta.page || 1;
          this.pagination.totalPages = data.meta.totalPages || 1;
          this.pagination.totalItems = data.meta.totalItems || 0;
        }
        
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load destinations';
        console.error('Error loading destinations:', err);
        this.loading = false;
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
        this.totalDestinations = data.total || 0;
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
