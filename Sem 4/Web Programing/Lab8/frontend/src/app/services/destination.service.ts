import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://localhost:8080/api/v1';

@Injectable({
  providedIn: 'root'
})
export class DestinationService {

  constructor(private http: HttpClient) { }

  getDestinations(page: number = 1, limit: number = 10, filters: any = {}): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('limit', limit.toString());

    if (filters.search) {
      params = params.set('search', filters.search);
    }

    if (filters.min_cost !== undefined) {
      params = params.set('min_cost', filters.min_cost.toString());
    }

    if (filters.max_cost !== undefined) {
      params = params.set('max_cost', filters.max_cost.toString());
    }

    if (filters.countries && filters.countries.length > 0) {
      params = params.set('countries', filters.countries.join(','));
    }

    return this.http.get(`${API_URL}/destinations.php`, { params });
  }

  getDestination(id: number): Observable<any> {
    return this.http.get(`${API_URL}/destinations.php?id=${id}`);
  }

  addDestination(destination: any): Observable<any> {
    const destinationData = {
      name: destination.name,
      country: destination.country_name, 
      description: destination.description,
      tourist_targets: destination.tourist_targets || '',
      cost_per_day: destination.cost_per_day
    };
    
    return this.http.post(`${API_URL}/destinations.php`, destinationData);
  }

  updateDestination(id: number, destination: any): Observable<any> {
    const destinationData = {
      name: destination.name,
      country: destination.country_name, 
      description: destination.description,
      tourist_targets: destination.tourist_targets || destination.attractions || '',
      cost_per_day: destination.cost_per_day || destination.cost
    };
    
    return this.http.put(`${API_URL}/destinations.php?id=${id}`, destinationData);
  }

  deleteDestination(id: number): Observable<any> {
    return this.http.delete(`${API_URL}/destinations.php?id=${id}`);
  }

  getCountries(): Observable<any> {
    return this.http.get(`${API_URL}/countries.php?with_destinations=true`);
  }

  getCostRange(): Observable<any> {
    return this.http.get(`${API_URL}/destinations.php?action=cost-range`);
  }
  
  getDestinationsCount(): Observable<any> {
    return this.http.get(`${API_URL}/destinations-num.php`);
  }
}
