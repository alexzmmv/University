import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, ActivatedRoute, Router } from '@angular/router';
import { DestinationService } from '../../services/destination.service';

@Component({
  selector: 'app-destination-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './destination-detail.component.html',
  styleUrl: './destination-detail.component.css'
})
export class DestinationDetailComponent implements OnInit {
  destination: any = {};
  error: string | null = null;
  success: string | null = null;
  showDeleteConfirm = false; 
  isLoading = true;

  constructor(
    private destinationService: DestinationService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['success']) {
        this.success = params['success'];
      }
    });
    
    // Get destination ID from route
    this.route.params.subscribe(params => {
      const id = +params['id'];
      this.loadDestination(id);
    });
  }

  loadDestination(id: number): void {
    this.isLoading = true;
    
    this.destinationService.getDestination(id).subscribe({
      next: (data) => {
        this.destination = data;
        
        if (!this.destination.tourist_targets && this.destination.touristTargets) {
          this.destination.tourist_targets = this.destination.touristTargets;
        }
        
        if (!this.destination.cost_per_day && this.destination.costPerDay) {
          this.destination.cost_per_day = this.destination.costPerDay;
        }
        
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Error loading destination. It may have been deleted or does not exist.';
        console.error('Error fetching destination:', error);
        this.isLoading = false;
      }
    });
  }

  showDeleteModal(): void {
    this.showDeleteConfirm = true;
  }

  hideDeleteModal(): void {
    this.showDeleteConfirm = false;
  }

  deleteDestination(): void {
    this.destinationService.deleteDestination(this.destination.id).subscribe({
      next: () => {
        this.router.navigate(['/destinations'], { 
          queryParams: { 
            success: `Destination "${this.destination.name}" was successfully deleted.` 
          }
        });
      },
      error: (error) => {
        this.error = 'Error deleting destination. Please try again.';
        this.showDeleteConfirm = false;
        console.error('Error deleting destination:', error);
      }
    });
  }
}
