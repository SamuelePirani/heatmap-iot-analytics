import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import GeoJSON from 'ol/format/GeoJSON';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'client';
  isBrowser: boolean;

  floors = [
    { id: 'floor1', name: 'First Floor', geoJsonUrl: './assets/geoJsonFloor/FirstFloor.geojson' },
    { id: 'floor2', name: 'Second Floor', geoJsonUrl: './assets/geoJsonFloor/SecondFloor.geojson' },
  ];

  constructor(@Inject(PLATFORM_ID) private platformId: Object, private http: HttpClient) {
    this.isBrowser = isPlatformBrowser(this.platformId);
    this.loadRooms(this.selectedFloor);
  }

  selectedFloor = this.floors[0].geoJsonUrl;
  rooms: string[] = [];
  selectedRoom: string = '';

  loadRooms(geoJsonUrl: string) {
    this.http.get(geoJsonUrl).subscribe((data: any) => {
      const features = new GeoJSON().readFeatures(data);
      this.rooms = features
        .filter((feature: any) => feature.get('type') === 'Room')
        .map((feature: any) => feature.get('name'));
    });
  }

  onFloorChange(event: any) {
    this.loadRooms(this.selectedFloor);
    this.selectedRoom = "";
  }
}
