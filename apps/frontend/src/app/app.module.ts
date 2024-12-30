import { CUSTOM_ELEMENTS_SCHEMA, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {AppLayoutModule} from './layout/app.layout.module';
import { OverviewComponent } from './pages/overview/overview.component';
import { MigrationComponent } from './pages/migration/migration.component';
import { ConfigComponent } from './pages/config/config.component';
import { LogsComponent } from './pages/logs/logs.component';
import { SimulationComponent } from './pages/simulation/simulation.component';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';

@NgModule({
  declarations: [
    AppComponent,
    OverviewComponent,
    MigrationComponent,
    ConfigComponent,
    LogsComponent,
    SimulationComponent
  ],
  imports: [
    CommonModule, 
    AppRoutingModule, 
    AppLayoutModule,
    TableModule, 
    ButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
