import { Component, OnDestroy, OnInit } from '@angular/core';
import { K8sService } from '../../service/k8s.service';
import { catchError, interval, map, Observable, of, startWith, Subject, switchMap, take, takeUntil, tap } from 'rxjs';
import { Pod, PodsResponse } from '../../model/k8s.model';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrl: './overview.component.scss'
})
export class OverviewComponent implements OnInit, OnDestroy{
  
  public podsCluster1!: Pod[];
  public podsCluster2!: Pod[];
  private destroy$ = new Subject<void>();


  constructor(private k8sService: K8sService) {}

  public ngOnInit(): void {
    this.getPodsCluster1()
    this.getPodsCluster2()
  }

  public ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }


  private getPodsCluster1() {
    interval(5000) // Emit every 5 seconds
      .pipe(
        startWith(0), // Start immediately
        switchMap(() =>
          this.k8sService.getPods('cluster1').pipe(
            map((podResponse: PodsResponse) => {
              console.log(podResponse.pods);
              return podResponse.pods;
            }),
            catchError(() => {
              return of([] as Pod[]);
            })
          )
        ),
        takeUntil(this.destroy$)
      )
      .subscribe((pods: Pod[]) => {
        this.podsCluster1 = pods;
      });
  }

  private getPodsCluster2() {
    interval(5000) // Emit every 5 seconds
      .pipe(
        startWith(0), // Start immediately
        switchMap(() =>
          this.k8sService.getPods('cluster2').pipe(
            map((podResponse: PodsResponse) => {
              return podResponse.pods;
            }),
            catchError(() => {
              return of([] as Pod[]);
            })
          )
        ),
        takeUntil(this.destroy$)
      )
      .subscribe((pods: Pod[]) => {
        this.podsCluster2 = pods;
      });
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
      catchError((error: any) => {
        console.error(`Failed to delete pod ${podName} in cluster ${cluster}:`, error);
        return of(error);
      })
    ).subscribe();
  }
}
