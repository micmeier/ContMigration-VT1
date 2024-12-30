export interface MigrationRequest {
    source_cluster: string;
    target_cluster: string;
    pod_name: string;
    generate_forensic_report: boolean;
    generate_AI_suggestion: boolean;
}