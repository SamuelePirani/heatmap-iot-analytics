import {Component, Inject, PLATFORM_ID} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {isPlatformBrowser} from '@angular/common';
import GeoJSON from 'ol/format/GeoJSON';
import {DataService} from "./data.service";
import {LoginComponent} from './login/login.component';
import {NbDialogService} from '@nebular/theme';
import {WebService} from '../services/web.service';

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
  value = 0;

  floors: Floor[] = [
    {id: 'floor1', name: 'First Floor', geoJsonUrl: './assets/geoJsonFloor/FirstFloor.geojson'},
    {id: 'floor2', name: 'Second Floor', geoJsonUrl: './assets/geoJsonFloor/SecondFloor.geojson'},
  ];

  sensors: string[] = ['Temperature', 'Humidity', 'CO2', 'Light', 'Pir'];

  intervals: number[] = [30, 60]

  selectedFloor: string = this.floors[0].geoJsonUrl;
  rooms: string[] = [];
  selectedRoom: string = '';

  startSelectedDate: Date | null = null;
  endSelectedDate: Date | null = null;

  loading = false;

  selectedSensor: string | null = null;
  selectedInterval: number = 0;

  minDate: Date = new Date('2025-3-10');
  maxDate: Date = new Date('2025-3-20');

  queryResponse: any = null;

  valueArray: string[] = [];
  sliderIndex: number = 0;

  constructor(
    @Inject(PLATFORM_ID) private readonly platformId: object,
    private readonly http: HttpClient,
    private readonly dataService: DataService,
    private dialogService: NbDialogService,
    private webService: WebService
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);
    this.fetchRooms(this.selectedFloor);

    try {
      this.webService.getRange().subscribe(
        next => {
          this.maxDate = new Date(next['max_end_date']);
          this.minDate = new Date(next['min_start_date']);
        }
      )
    } catch (error) {
      console.error("Error fetching range data:", error);
    }
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
    console.log("Changed Floor:", this.selectedFloor);
    this.selectedRoom = '';
    this.fetchRooms(newFloorUrl);
  }

  openLoginModal(): void {
    this.dialogService.open(LoginComponent);
  }

  onStartDateChange(event: any): void {
    this.startSelectedDate = event;
    console.log("Start Date:", this.startSelectedDate);
  }

  onEndDateChange(event: any): void {
    this.endSelectedDate = event;
    console.log("End Date:", event);
  }

  onQueryButtonClick(): void {
    this.toggleLoadingAnimation()
    if (!this.selectedFloor) {
      alert('Please select a floor');
      return;
    }
    if (!this.startSelectedDate || !this.endSelectedDate) {
      alert('Please select start and end dates');
      return;
    }
    if (!this.selectedSensor) {
      alert('Please select a sensor');
      return
    }
    if (!this.intervals.includes(this.selectedInterval)) {
      alert('Please select a time interval');
      return
    }
    const data = {
      'start_date': this.startSelectedDate,
      'end_date': this.endSelectedDate,
      'sensor': this.selectedSensor,
      'interval': this.selectedInterval,
      'room': this.selectedRoom
    }
    console.log("Query Data:", data);
    this.webService.getQuery(
      this.startSelectedDate.toISOString(),
      this.endSelectedDate.toISOString(),
      this.selectedRoom,
      this.selectedSensor,
      this.selectedInterval
    ).subscribe(
      next => {
        this.queryResponse = next;
        const uniqueValues = new Set();
        if (this.queryResponse) {
          this.queryResponse.forEach(
              (element: any) => {
              if (element.start) {
                uniqueValues.add(element.start);
              }
            }
          )
        }
        this.valueArray = Array.from(uniqueValues) as string[];
        console.log("Query Response:", this.queryResponse);
      }
    )
  }

  toggleLoadingAnimation(): void {
    this.loading = true;
    setTimeout(() => this.loading = false, 3000);
  }

  onTimeIntervalChange(value: any): void {
    console.log("Time Interval:", value);
    this.selectedInterval = value;
  }

  onSensorChange(value: any): void {
    console.log("Sensor:", value.value);
    this.selectedSensor = value.value;
  }

  getSliderValue(): string {
    return this.valueArray[this.sliderIndex];
  }

  onSliderChange(event: any) {
    this.sliderIndex = event.value;
  }
}
