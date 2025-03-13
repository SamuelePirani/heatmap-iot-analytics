import {NgModule} from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {BrowserModule, provideClientHydration, withEventReplay} from '@angular/platform-browser'
import {AppComponent} from './app.component';
import {NbButtonModule, NbLayoutModule, NbSelectModule, NbSidebarModule, NbThemeModule} from '@nebular/theme';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {provideHttpClient} from '@angular/common/http';
import {NgOptimizedImage} from '@angular/common';

@NgModule({
    declarations: [
        AppComponent,
        HeatmapComponent
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        NbThemeModule.forRoot({name: 'dark'}),
        NbLayoutModule,
        NbSelectModule,
        NbSidebarModule.forRoot(),
        NbButtonModule,
        NgOptimizedImage,
    ],
    providers: [
        provideClientHydration(withEventReplay()),
        provideHttpClient()
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
