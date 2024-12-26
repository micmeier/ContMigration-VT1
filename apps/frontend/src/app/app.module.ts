import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {AppLayoutModule} from './layout/app.layout.module';
import { HeaderComponent } from './header/header.component';
import { OverviewComponent } from './pages/overview/overview.component';
import { MigrationComponent } from './pages/migration/migration.component';
import { ConfigComponent } from './pages/config/config.component';
import { LogsComponent } from './pages/logs/logs.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    OverviewComponent,
    MigrationComponent,
    ConfigComponent,
    LogsComponent
  ],
  imports: [
    AppRoutingModule, AppLayoutModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
