export interface Pod {
    podName?: string;
    appName?: string;
    status?: string;
    reason?: string;
  }
  
export interface PodsResponse {
  pods: Pod[];
}