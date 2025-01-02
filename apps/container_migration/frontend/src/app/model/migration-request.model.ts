export interface MigrationRequest {
    sourceCluster: string;
    targetCluster: string;
    podName: string;
    appName: string;
    forensicAnalysis: boolean;
    AISuggestion: boolean;
}