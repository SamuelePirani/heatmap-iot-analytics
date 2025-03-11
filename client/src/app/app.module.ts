import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser'
import { AppComponent } from './app.component';
import { NbThemeModule, NbSidebarModule, NbLayoutModule, NbButtonModule } from '@nebular/theme';




@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    NbThemeModule.forRoot({name:'dark'}),
    NbLayoutModule,
    NbSidebarModule.forRoot(),
    NbButtonModule
  ],
  providers: [
    provideClientHydration(withEventReplay())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
