import { Component, OnInit } from '@angular/core';
import { K8sService } from '../../service/k8s.service';
import { catchError, interval, map, Observable, of, startWith, switchMap, take, tap } from 'rxjs';
import { Pod, PodsResponse } from '../../model/k8s.model';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrl: './overview.component.scss'
})
export class OverviewComponent implements OnInit{
  
  public podsCluster1$!: Observable<Pod[]>;
  public podsCluster2$!: Observable<Pod[]>;
  constructor(private k8sService: K8sService) {}

  public ngOnInit(): void {
    this.getPodsCluster1()
    this.getPodsCluster2()
  }


  private getPodsCluster1() {
    this.podsCluster1$ = interval(5000) // Polling every 5 seconds
      .pipe(
        startWith(0),
        switchMap(() =>
          this.k8sService.getPods('cluster1').pipe(
            map((podResponse: PodsResponse) => {
              console.log(podResponse.pods);
              return podResponse.pods;
            }),
            catchError(() => {
              return of([{}] as Pod[]);
            })
          )
        )
      );
  }

  private getPodsCluster2() {
    this.podsCluster2$ = interval(5000) // Polling every 5 seconds
      .pipe(
        startWith(0),
        switchMap(() =>
          this.k8sService.getPods('cluster2').pipe(
            map((podResponse: PodsResponse) => {
              return podResponse.pods;
            }),
            catchError(() => {
              return of([{}] as Pod[]);
            })
          )
        )
      );
  }

  public deletePod(cluster: string, podName: string): void {
    this.k8sService.deletePod(cluster, podName).pipe(
      take(1), // Ensures only one emission is taken
      tap(() => {
        console.log(`Pod ${podName} in cluster ${cluster} deleted successfully.`);
        if(cluster === 'cluster1') {
          this.getPodsCluster1();
        } else if (cluster === 'cluster2') {
          this.getPodsCluster2();
        }
      }),
      catchError((error) => {
        console.error(`Failed to delete pod ${podName} in cluster ${cluster}:`, error);
        return of(error);
      })
    ).subscribe();
  }
}
