import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { PodsResponse } from '../model/k8s.model';
import { MigrationRequest } from '../model/migration-request.model';
import { TreeNode } from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class K8sService {

  private apiUrl = 'http://160.85.255.146:8000'; // Change this to your FastAPI server URL

  constructor(private http: HttpClient) {}

  /**
   * Get a list of pods and their statuses from the specified cluster.
   * @param cluster The name of the cluster (e.g., 'cluster1' or 'cluster2')
   * @returns Observable containing the pods data as PodsResponse.
   */
  getPods(cluster: string): Observable<PodsResponse> {
    const url = `${this.apiUrl}/k8s/pods/${cluster}`;
    return this.http.get<PodsResponse>(url);
  }

    /**
   * Delete a pod with the specified name from the specified cluster.
   * @param cluster The name of the cluster (e.g., 'cluster1' or 'cluster2')
   * @param podName The name of the pod (e.g., 'cpu-restore')
   * @returns Observable containing the pods data as PodsResponse.
   */
  deletePod(cluster: string, podName: string): Observable<void> {
    const url = `${this.apiUrl}/k8s/pods/${cluster}/${podName}`;
    return this.http.delete<void>(url);
  }

  migratePod(request: MigrationRequest): Observable<void> {
    const url = `${this.apiUrl}/migrate`;
    return this.http.post<void>(url, request);
  }

  getLogStructure(): Observable<TreeNode[]> {
    const url = `${this.apiUrl}/directory-structure`;
    return this.http.get<{ data: TreeNode[] }>(url).pipe(
      map(response => response.data as TreeNode[])
    );
  }

  viewFile(file: TreeNode): Observable<string> {
    const url = `${this.apiUrl}/view/${file.data}`;
    return this.http.get<any>(url).pipe(
      map(response => response.content)
    );
  }

  downloadFile(file: TreeNode): Observable<Blob> {
    const url = `${this.apiUrl}/download/${file.data}`;
    return this.http.get(url, { responseType: 'blob' });
  }

}