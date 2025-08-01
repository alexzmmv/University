import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, LoginRequest } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginData: LoginRequest = {
    username: '',
    password: ''
  };
  
  loading = false;
  error: string | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.error = null;
    
    if (!this.validateForm()) {
      return;
    }

    this.loading = true;
    
    this.authService.login(this.loginData).subscribe({
      next: (response) => {
        this.loading = false;
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 401) {
          this.error = 'Invalid username or password';
        } else {
          this.error = 'Login failed. Please try again.';
        }
        console.error('Login error:', err);
      }
    });
  }

  validateForm(): boolean {
    if (!this.loginData.username.trim()) {
      this.error = 'Username is required';
      return false;
    }
    
    if (!this.loginData.password) {
      this.error = 'Password is required';
      return false;
    }
    
    return true;
  }
}
