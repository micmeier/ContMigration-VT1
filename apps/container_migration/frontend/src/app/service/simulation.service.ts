import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SimulationRequest } from '../model/simulation-request.model';

@Injectable({
  providedIn: 'root'
})
export class SimulationService {
    private apiUrl = 'http://160.85.255.146:8000'; // Replace with your actual API URL

    constructor(private http: HttpClient) {}

    triggerSimulation(appName: string, attackType: string): Observable<void> {
        const url = `${this.apiUrl}/simulate`;
        const body: SimulationRequest = {
            "appName": appName, 
            "attackType": attackType
        };
        return this.http.post<void>(url, body);
    }
}