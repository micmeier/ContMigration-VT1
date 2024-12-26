import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {OverviewComponent} from './pages/overview/overview.component';
import {MigrationComponent} from './pages/migration/migration.component';
import {LogsComponent} from './pages/logs/logs.component';
import {ConfigComponent} from './pages/config/config.component';

const routes: Routes = [
  {
    path: '', component: OverviewComponent,
  },
  {
    path: 'migration', component: MigrationComponent,
  },
  {
    path: 'logs', component: LogsComponent,
  },
  {
    path: 'config', component: ConfigComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
