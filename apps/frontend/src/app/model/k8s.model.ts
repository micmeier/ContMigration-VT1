export interface Pod {
    name: string;
    status: string;
  }
  
  export interface PodsResponse {
    pods: Pod[];
  }