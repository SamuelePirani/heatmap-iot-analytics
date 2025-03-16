import {NgModule} from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {BrowserModule, provideClientHydration, withEventReplay} from '@angular/platform-browser'
import {AppComponent} from './app.component';

import {
  NbButtonModule, NbCardModule, NbFormFieldModule, NbIconModule,
  NbInputModule,
  NbLayoutModule,
  NbSelectModule,
  NbSidebarModule,
  NbThemeModule,
  NbDatepickerModule, NbSpinnerModule, NbToastrModule
} from '@nebular/theme';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {provideHttpClient} from '@angular/common/http';
import {NgOptimizedImage} from '@angular/common';
import { LoginComponent } from './login/login.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterOutlet} from '@angular/router';
import { NbDialogModule } from '@nebular/theme';
import {NbEvaIconsModule} from '@nebular/eva-icons';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeng/themes/aura';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { SliderModule } from 'primeng/slider';
import {InputText} from 'primeng/inputtext';


@NgModule({
    declarations: [
        AppComponent,
        HeatmapComponent,
        LoginComponent
    ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    NbThemeModule.forRoot({name: 'dark'}),
    NbLayoutModule,
    NbSelectModule,
    NbInputModule,
    NbIconModule,
    NbDialogModule.forRoot(),
    NbSidebarModule.forRoot(),
    NbButtonModule,
    NgOptimizedImage,
    ReactiveFormsModule,
    RouterOutlet,
    NbCardModule,
    NbFormFieldModule,
    NbEvaIconsModule,
    NbIconModule,
    SliderModule,
    FormsModule,
    NbDatepickerModule.forRoot(),
    NbSpinnerModule,
    InputText,
    NbToastrModule.forRoot()
  ],
    providers: [
        provideClientHydration(withEventReplay()),
        provideHttpClient(),
        provideAnimationsAsync(),
        providePrimeNG({
          theme: {
            preset: Aura
          }
        })
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
