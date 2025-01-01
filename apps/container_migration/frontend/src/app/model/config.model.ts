export interface RuleConfig {
    rule: string;
    cluster: string;
    action: string;
    targetCluster?: string | null;
    forensic_analysis: boolean;
    AI_suggestion: boolean;
}

export interface Config {
    config: RuleConfig[];
}