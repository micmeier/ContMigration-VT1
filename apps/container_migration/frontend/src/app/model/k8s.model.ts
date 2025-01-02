export interface Pod {
    podName?: string;
    appName?: string;
    status?: string;
    reason?: string;
    age?: string;
  }
  
export interface PodsResponse {
  pods: Pod[];
}