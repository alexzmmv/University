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
      // Ensure we're sending a comma-separated list of country IDs
      const countriesStr = filters.countries.join(',');
      console.log('Sending countries filter:', countriesStr);
      params = params.set('countries', countriesStr);
    } else {
      console.log('No countries filter applied');
    }

    return this.http.get(`${API_URL}/destinations`, { params });
  }

  getDestination(id: number): Observable<any> {
    return this.http.get(`${API_URL}/destinations/${id}`);
  }

  addDestination(destination: any): Observable<any> {
    const destinationData = {
      name: destination.name,
      country: destination.country_name, 
      description: destination.description,
      touristTargets: destination.tourist_targets || '',
      costPerDay: destination.cost_per_day
    };
    
    return this.http.post(`${API_URL}/destinations`, destinationData);
  }

  updateDestination(id: number, destination: any): Observable<any> {
    const destinationData = {
      name: destination.name,
      country: destination.country_name,
      description: destination.description,
      touristTargets: destination.tourist_targets || destination.attractions || '',
      costPerDay: destination.cost_per_day || destination.cost
    };
    
    return this.http.put(`${API_URL}/destinations/${id}`, destinationData);
  }

  deleteDestination(id: number): Observable<any> {
    return this.http.delete(`${API_URL}/destinations/${id}`);
  }

  getCountries(): Observable<any> {
    const params = new HttpParams().set('with_destinations', 'true');
    return this.http.get(`${API_URL}/countries`, { params });
  }

  getCostRange(): Observable<any> {
    return this.http.get(`${API_URL}/destinations/cost-range`);
  }
  
  getDestinationsCount(): Observable<any> {
    return this.http.get(`${API_URL}/destinations/count`);
  }
}
