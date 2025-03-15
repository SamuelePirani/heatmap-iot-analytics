import {Component, Inject, PLATFORM_ID, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {isPlatformBrowser} from '@angular/common';
import GeoJSON from 'ol/format/GeoJSON';
import {DataService} from "./data.service";
import {LoginComponent} from './login/login.component';
import {NbDialogService} from '@nebular/theme';
import {WebService} from '../services/web.service';
import {HeatmapComponent} from './heatmap/heatmap.component';

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

  minDate: Date | null = null;
  maxDate: Date | null = null;

  selectedStartDate = this.minDate;
  selectedEndDate = this.maxDate;

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
    this.selectedSensor = 'Temperature';
    this.selectedInterval = 30;

    try {
      this.webService.getRange().subscribe(
        next => {
          const max = new Date(next['max_end_date']);
          const min = new Date(next['min_start_date']);
          this.maxDate = max;
          this.minDate = min;
          this.selectedStartDate = this.minDate;
          this.selectedEndDate = this.maxDate;
          this.onStartDateChange(min)
          this.onEndDateChange(max)
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

  onStartDateChange(event: any): void {
    this.startSelectedDate = event;
    console.log("Start Date:", this.startSelectedDate);
  }

  onEndDateChange(event: any): void {
    this.endSelectedDate = event;
    console.log("End Date:", event);
  }

  @ViewChild(HeatmapComponent) heatmapComponent?: HeatmapComponent;

  onQueryButtonClick(): void {
    this.toggleLoadingAnimation()
    if (!this.selectedFloor) {
      alert('Please select a floor');
      return;
    }
    if (!this.startSelectedDate || !this.endSelectedDate) {
      alert('Please select start and end dates, current values are: ' + this.startSelectedDate + ' ' + this.endSelectedDate);
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
    this.queryResponse = null;
    this.webService.getQuery(
      this.startSelectedDate.toISOString(),
      this.endSelectedDate.toISOString(),
      this.selectedRoom,
      this.selectedSensor,
      this.selectedInterval
    ).subscribe(
      next => {
        this.queryResponse = next;
        if (this.queryResponse) {
          this.queryResponse.forEach(
            (element: any) => {
              if (element.start) {
                if (!this.valueArray.includes(element.start)) {
                  this.valueArray.push(element.start);
                }
              }
            }
          )
        }
        this.min = Infinity;
        this.max = -Infinity;
        this.updateMinAndMaxValuesFromData(this.queryResponse, this.getSelectedSensor());
        this.updateHeatmap();
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
    if (this.queryResponse) {
      this.min = Infinity;
      this.max = -Infinity;
      this.updateMinAndMaxValuesFromData(this.queryResponse, this.getSelectedSensor());
      this.updateHeatmap();
    }
  }

  getSliderValue(): string {
    return this.valueArray[this.sliderIndex];
  }

  onSliderChange(event: any) {
    this.sliderIndex = event.value;
    this.updateHeatmap()
  }

  private getSelectedSensor(): string {
    return this.selectedSensor?.toLowerCase() ?? '';
  }

  private updateHeatmap(): void {
    if (this.heatmapComponent) {
      this.heatmapComponent.createHeatmap(this.queryResponse, this.getSelectedSensor(), this.getSliderValue() ?? '', this.min, this.max);
    }
  }

  min = Infinity
  max = -Infinity

  private updateMinAndMaxValuesFromData(data: any[], selectedSensor: string): void {
    data.forEach((item) => {
      const sensors = item['sensors']
      for (let i = 0; i < sensors.length; i++) {
        const sensorsData = sensors[i]
        if (sensorsData['type'] === selectedSensor) {
          this.min = Math.min(this.min, sensorsData['min'])
          this.max = Math.max(this.max, sensorsData['max'])
        }
      }
    })
  }
}
