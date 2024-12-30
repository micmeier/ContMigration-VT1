import { Component, OnInit } from '@angular/core';
import { SelectItem } from 'primeng/api';
import { K8sService } from '../../service/k8s.service';
import { catchError, map, of, take, tap } from 'rxjs';
import { PodsResponse } from '../../model/k8s.model';
import { MigrationRequest } from '../../model/migration-request.model';

@Component({
  selector: 'app-migration',
  templateUrl: './migration.component.html',
  styleUrl: './migration.component.scss'
})
export class MigrationComponent implements OnInit{
  
  sourceCluster: SelectItem[] = [];
  targetCluster: SelectItem[] = [];
  podsCluster1: SelectItem[] = [];
  selectedSource: string = '';
  selectedTarget: string = '';
  selectedPod: string = '';
  isGeneratingFA = false;
  isGeneratingAISuggestion = false;

  constructor(private k8sService: K8sService) {}
  ngOnInit(): void {
    
    this.sourceCluster = [
      { label: 'Cluster 1', value: 'cluster1' }
    ];

    this.targetCluster = [
      { label: 'Cluster 2', value: 'cluster2' }
    ];

    this.getPodsCluster1();
  }

  private getPodsCluster1() {
    this.k8sService.getPods('cluster1').pipe(
      map((podResponse: PodsResponse) => {
        return podResponse.pods
          .filter(pod => pod.status === 'Running')
          .map(pod => ({ label: pod.name, value: pod.name } as SelectItem));
      }),
      catchError(() => {
        return of([] as SelectItem[]);
      })
    ).subscribe((pods: SelectItem[]) => {
      this.podsCluster1 = pods;
    });
  }

  public reset(): void {
    this.selectedSource = '';
    this.selectedTarget = '';
    this.selectedPod = '';
    this.isGeneratingFA = false;
    this.isGeneratingAISuggestion = false;
  }

  public areDropdownsFilled(): boolean {
    return this.selectedSource !== '' && this.selectedTarget !== '';
  }

  public migratePod(): void {
    const migrationRequest: MigrationRequest = {
      source_cluster: this.selectedSource,
      target_cluster: this.selectedTarget,
      pod_name: this.selectedPod,
      generate_forensic_report: this.isGeneratingFA,
      generate_AI_suggestion: this.isGeneratingAISuggestion
    };
    this.k8sService.migratePod(migrationRequest).pipe(
      take(1), // Ensures only one emission is taken
      tap((response) => {
        console.log('Pod migration successful:', response);
      }),
      catchError((error) => {
        console.error('Pod migration failed:', error);
        return of(error);
      })
    ).subscribe();
  }
  


}
