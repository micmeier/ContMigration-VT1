import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { TreeNode } from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class LogsService {
    private apiUrl = 'http://160.85.255.146:8000'; // Replace with your actual API URL

    constructor(private http: HttpClient) {}

    getLogStructure(): Observable<TreeNode[]> {
        const url = `${this.apiUrl}/logs/structure`;
        return this.http.get<{ data: TreeNode[] }>(url).pipe(
            map((response: { data: any; }) => response.data)
        );
    }

    viewFile(file: TreeNode): Observable<string> {
        const url = `${this.apiUrl}/logs/view/${file.data}`;
        return this.http.get<{ content: string }>(url).pipe(
            map((response: { content: any; }) => response.content)
        );
    }

    downloadFile(file: TreeNode): Observable<Blob> {
        const url = `${this.apiUrl}/logs/download/${file.data}`;
        return this.http.get(url, { responseType: 'blob' });
    }
}