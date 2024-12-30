import { Component, OnInit } from '@angular/core';
import { K8sService } from '../../service/k8s.service';
import { MenuItem, MessageService, TreeNode } from 'primeng/api';

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrl: './logs.component.scss'
})
export class LogsComponent implements OnInit {
  
  files: TreeNode[] = [];
  items: MenuItem[] = [];
  selectedFile!: TreeNode;
  viewFileContent: string = '';
  viewedLabel: string = '';
  
  constructor(private k8sService: K8sService, private messageService: MessageService) {}

  ngOnInit(): void {
    this.getLogStructure();
    this.items = [
      {label: 'View', icon: 'pi pi-search', command: (event) => this.viewFile(this.selectedFile)},
      {label: 'Download', icon: 'pi pi-download', command: (event) => this.downloadFile(this.selectedFile)}
    ];
  }

  private getLogStructure() {
    this.k8sService.getLogStructure().subscribe((data: TreeNode[]) => {
      this.files = data;
    });
  }

  viewFile(file: TreeNode) {
    if (file.label && file.label.endsWith('.txt')) {
      this.k8sService.viewFile(file).subscribe((content: string) => {
        this.viewFileContent = content;
        this.viewedLabel = file.label!;
      });
    } else {
      this.messageService.add({severity:'error', summary: 'Error', detail: 'Only text files can be viewed.'});
    }
  }

  nodeSelect(event: any) {
    if(event.node.label !== this.viewedLabel) {
      this.viewFileContent = '';
    }
  }

  downloadFile(file: TreeNode) {
    if(file.label && file.label.endsWith('.txt')) {
      this.k8sService.downloadFile(file).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.label!;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    };
  }
}
