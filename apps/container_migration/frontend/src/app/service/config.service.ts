import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { SelectItem, TreeNode } from 'primeng/api';
import { Config, RuleConfig } from '../model/config.model';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
    private apiUrl = 'http://160.85.255.146:8000'; // Replace with your actual API URL

    constructor(private http: HttpClient) {}

    getConfig(): Observable<RuleConfig[]> {
        const url = `${this.apiUrl}/config`;
        return this.http.get<Config>(url).pipe(
          map((config: Config) => config.config)
        );
      }
    
    addRule(ruleConfig: RuleConfig): Observable<any> {
        const url = `${this.apiUrl}/config`;
        return this.http.post(url, ruleConfig);
    }
    
    deleteRuleByIndex(index: number): Observable<any> {
        const url = `${this.apiUrl}/config/${index}`;
        return this.http.delete(url);
    }

    getFalcoRules(): Observable<SelectItem[]> {
        return this.http.get('/assets/default_falco_rules.txt', { responseType: 'text' }).pipe(
          map((data: string) => data.split('\n').map(line => line.trim()).filter(line => line.length > 0)),
          map((lines: string[]) => lines.map(line => ({ label: line, value: line })))
        );
    }
}