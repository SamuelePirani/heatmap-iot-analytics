import {Component, Inject, PLATFORM_ID} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {isPlatformBrowser} from '@angular/common';
import GeoJSON from 'ol/format/GeoJSON';
import {DataService} from "./data.service";

interface Floor {
    id: string;
    name: string;
    geoJsonUrl: string;
}

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    standalone: false,
    styleUrl: './app.component.scss',
})
export class AppComponent {
    isBrowser: boolean;

    floors: Floor[] = [
        {id: 'floor1', name: 'First Floor', geoJsonUrl: './assets/geoJsonFloor/FirstFloor.geojson'},
        {id: 'floor2', name: 'Second Floor', geoJsonUrl: './assets/geoJsonFloor/SecondFloor.geojson'},
    ];

    selectedFloor: string = this.floors[0].geoJsonUrl;
    rooms: string[] = [];
    selectedRoom: string = '';

    constructor(
        @Inject(PLATFORM_ID) private readonly platformId: object,
        private readonly http: HttpClient,
        private readonly dataService: DataService
    ) {
        this.isBrowser = isPlatformBrowser(this.platformId);
        this.fetchRooms(this.selectedFloor);
    }

    fetchRooms(geoJsonUrl: string): void {
        this.http.get(geoJsonUrl).subscribe((data: unknown) => {
            const geoJsonFeatures = new GeoJSON().readFeatures(data);
            this.rooms = geoJsonFeatures
                .filter((feature: any) => feature.get('type') === 'Room')
                .map((feature: any) => feature.get('name'));
        });
    }

    onFloorChange(newFloorUrl: string): void {
        this.selectedFloor = newFloorUrl;
        this.selectedRoom = '';
        this.fetchRooms(newFloorUrl);
    }
}