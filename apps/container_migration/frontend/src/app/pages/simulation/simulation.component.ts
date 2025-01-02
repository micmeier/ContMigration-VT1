import { Component, OnInit } from '@angular/core';
import { K8sService } from '../../service/k8s.service';
import { SelectItem } from 'primeng/api';
import { catchError, map, of } from 'rxjs';
import { PodsResponse } from '../../model/k8s.model';

@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrl: './simulation.component.scss'
})
export class SimulationComponent implements OnInit{
  
  targetPod: SelectItem[] = [];
  attackType: SelectItem[] = [];
  selectedPod: string = '';
  selectedAttack: string = '';

  constructor(private k8sService: K8sService) {}

  ngOnInit(): void {
    this.attackType = [
      { label: 'Reverse shell', value: 'reverse_shell' },
      { label: 'Data destruction', value: 'data_destruction' },
      { label: 'Log file tempering', value: 'log_tempering' }
    ];

    this.getPodsCluster1();
  }

  private getPodsCluster1() {
      this.k8sService.getPods('cluster1').pipe(
        map((podResponse: PodsResponse) => {
            return podResponse.pods
            .filter(pod => pod.status === 'Running' && pod.podName!.startsWith('vuln-spring'))
            .map(pod => ({ label: pod.podName, value: pod.podName } as SelectItem));
        }),
        catchError(() => {
          return of([] as SelectItem[]);
        })
      ).subscribe((pods: SelectItem[]) => {
        this.targetPod = pods;
      });
    }

  public reset(): void {
    this.selectedPod = '';
    this.selectedAttack = '';
  }

  public simulateAttack(): void {
    //TODO: Implement method to simulate an this.attackType[Symbol]
    console.log("Simulating attack: " + this.selectedAttack + " on pod: " + this.selectedPod);
  }
  
  
}
