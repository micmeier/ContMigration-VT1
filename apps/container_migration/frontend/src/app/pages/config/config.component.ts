import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../../service/config.service';
import { catchError, filter, map, of, take, tap } from 'rxjs';
import { RuleConfig } from '../../model/config.model';
import { SelectItem } from 'primeng/api';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrl: './config.component.scss'
})
export class ConfigComponent implements OnInit {

  public config!: RuleConfig[];
  public isDialogVisible = false;
  public rulesSelection: SelectItem[] = [];
  public clusterSelection: SelectItem[] = [];
  public actionSelection: SelectItem[] = [];
  public targetClusterSelection: SelectItem[] = [];
  public selectedRule: string = '';
  public selectedCluster: string = '';
  public selectedAction: string = '';
  public selectedTargetCluster: string = '';
  public isGeneratingFA: boolean = false;
  public isGeneratingAISuggestion: boolean = false;

  constructor(private configService: ConfigService) { }

  ngOnInit(): void {
    this.getConfig();

    this.clusterSelection = [
      { label: 'Cluster 1', value: 'cluster1' }
    ];

    this.actionSelection = [
      { label: 'Migrate container', value: 'migrate' },
      { label: 'Log falco events', value: 'log' },
    ];

    this.targetClusterSelection = [
      { label: 'Cluster 2', value: 'cluster2' }
    ];

  }

  private getConfig() {
    this.configService.getConfig().pipe(
      take(1),
      catchError(() => {
        return of([] as RuleConfig[]);
      })
    ).subscribe((configs: RuleConfig[]) => {
      this.config = configs;
    });
  }

  private loadRules() {
    this.configService.getFalcoRules().pipe(
      tap((rules: SelectItem[]) => {
        console.log("Rules before filtering: ", rules);
      }),
      map((rules: SelectItem[]) => rules.filter(rule => !this.config.some(config => config.rule === rule.value)))
    ).subscribe((filteredRules: SelectItem[]) => {
      console.log("filered rules: ", filteredRules)
      this.rulesSelection = filteredRules;
    });
  }


  public showDialog(): void {
    this.isDialogVisible = true;
    this.loadRules();
  }

  public isMigrateActionSelected(): boolean {
    return this.selectedAction === 'migrate' && this.selectedCluster !== '' && this.selectedRule !== '';
  }

  public cancelDialog(): void {
    this.isDialogVisible = false;
    this.resetDialog();
  }

  public saveNewRule(): void {
    this.isDialogVisible = false;

    const ruleConfig: RuleConfig = {
      rule: this.selectedRule,
      cluster: this.selectedCluster,
      action: this.selectedAction,
      targetCluster: this.selectedTargetCluster,
      forensic_analysis: this.isGeneratingFA,
      AI_suggestion: this.isGeneratingAISuggestion
    };

    this.configService.addRule(ruleConfig).pipe(take(1)).subscribe(() => {
      this.resetDialog();
      this.getConfig();
    });
  }

  public deleteRule(index: number): void {
    this.configService.deleteRuleByIndex(index).pipe(take(1)).subscribe(() => {
      this.getConfig();
    });
  }

  private resetDialog(): void {
    this.selectedRule = '';
    this.selectedCluster = '';
    this.selectedAction = '';
    this.selectedTargetCluster = '';
    this.isGeneratingFA = false;
    this.isGeneratingAISuggestion = false;
  }
}
