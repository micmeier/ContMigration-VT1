import { Component, OnInit } from '@angular/core';
import { MenuItem, MessageService, TreeNode } from 'primeng/api';
import { LogsService } from '../../service/logs.service';

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
  
  constructor(private logService: LogsService, private messageService: MessageService) {}

  ngOnInit(): void {
    this.getLogStructure();
    this.items = [
      {label: 'View', icon: 'pi pi-search', command: (event) => this.viewFile(this.selectedFile)},
      {label: 'Download', icon: 'pi pi-download', command: (event) => this.downloadFile(this.selectedFile)}
    ];
  }

  private getLogStructure() {
    this.logService.getLogStructure().subscribe((data: TreeNode[]) => {
      this.files = data;
    });
  }

  viewFile(file: TreeNode) {
    if (file.label && file.label.endsWith('.txt')) {
      this.logService.viewFile(file).subscribe((content: string) => {
        this.viewFileContent = content;
        this.viewedLabel = file.label!;
      });
    } else {
      console.log("error")
      this.messageService.add({key: 'tst', severity:'error', summary: 'Error', detail: 'Only text files can be viewed.'});
    }
  }

  nodeSelect(event: any) {
    if(event.node.label !== this.viewedLabel) {
      this.viewFileContent = '';
    }
  }

  downloadFile(file: TreeNode) {
    if(file.label && file.label.endsWith('.txt')) {
      this.logService.downloadFile(file).subscribe((blob: any) => {
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
