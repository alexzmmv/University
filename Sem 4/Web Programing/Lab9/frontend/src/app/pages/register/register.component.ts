import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, RegisterRequest } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  registerData: RegisterRequest = {
    username: '',
    email: '',
    password: ''
  };
  
  confirmPassword = '';
  loading = false;
  error: string | null = null;
  success: string | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.error = null;
    this.success = null;
    
    if (!this.validateForm()) {
      return;
    }

    this.loading = true;
    
    this.authService.register(this.registerData).subscribe({
      next: (response) => {
        this.loading = false;
        this.success = 'Registration successful! You can now log in.';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err) => {
        this.loading = false;
        if (err.error && err.error.error) {
          this.error = err.error.error;
        } else {
          this.error = 'Registration failed. Please try again.';
        }
        console.error('Registration error:', err);
      }
    });
  }

  validateForm(): boolean {
    if (!this.registerData.username.trim()) {
      this.error = 'Username is required';
      return false;
    }
    
    if (this.registerData.username.length < 3) {
      this.error = 'Username must be at least 3 characters long';
      return false;
    }
    
    if (!this.registerData.email.trim()) {
      this.error = 'Email is required';
      return false;
    }
    
    if (!this.isValidEmail(this.registerData.email)) {
      this.error = 'Please enter a valid email address';
      return false;
    }
    
    if (!this.registerData.password) {
      this.error = 'Password is required';
      return false;
    }
    
    if (this.registerData.password.length < 6) {
      this.error = 'Password must be at least 6 characters long';
      return false;
    }
    
    if (this.registerData.password !== this.confirmPassword) {
      this.error = 'Passwords do not match';
      return false;
    }
    
    return true;
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}
