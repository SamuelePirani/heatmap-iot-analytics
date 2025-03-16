import {Component, Inject, PLATFORM_ID, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {isPlatformBrowser} from '@angular/common';
import GeoJSON from 'ol/format/GeoJSON';
import {WebService} from '../services/web.service';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {NbGlobalPhysicalPosition, NbToastrService} from '@nebular/theme';

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
  dataUnit: string = 'Temperature'

  constructor(
    @Inject(PLATFORM_ID) private readonly platformId: object,
    private readonly http: HttpClient,
    private toasterService: NbToastrService,
    private webService: WebService
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);
    this.fetchRooms(this.selectedFloor);
    this.selectedSensor = 'Temperature';
    this.selectedInterval = 30;
    this.webService.getRange().subscribe({
        next: (data: any) => {
          const max = new Date(data['max_end_date']);
          const min = new Date(data['min_start_date']);
          this.maxDate = max;
          this.minDate = min;
          this.selectedStartDate = this.minDate;
          this.selectedEndDate = this.maxDate;
          this.onStartDateChange(min)
          this.onEndDateChange(max)
        },
        error: (error: any) => {
          this.showErrorToast('Error fetching data ' + error, 'Server Error')
        }
      }
    )
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
    this.removeOldData()
  }

  onStartDateChange(event: any): void {
    this.startSelectedDate = event;
    this.removeOldData()
    console.log("Start Date:", this.startSelectedDate);
  }

  onEndDateChange(event: any): void {
    this.endSelectedDate = event;
    this.removeOldData();
    console.log("End Date:", event);
  }

  @ViewChild(HeatmapComponent) heatmapComponent?: HeatmapComponent;

  private getQueryParamsIfValid(): { start: string, end: string, room: string, interval: number } | null {
    if (!this.selectedFloor) {
      this.showErrorToast('Please select a floor', 'Missing Field')
      this.toggleLoadingAnimation()
      return null;
    }
    if (!this.startSelectedDate || !this.endSelectedDate) {
      this.showErrorToast('Please select start and end dates', 'Missing Field')
      this.toggleLoadingAnimation()
      return null;
    }
    if (!this.selectedSensor) {
      this.showErrorToast('Please select a sensor', 'Missing Field')
      this.toggleLoadingAnimation()
      return null;
    }
    if (!this.intervals.includes(this.selectedInterval)) {
      this.showErrorToast('Please select a time interval', 'Missing Field')
      this.toggleLoadingAnimation()
      return null
    }
    return {
      start: this.startSelectedDate.toISOString(),
      end: this.endSelectedDate.toISOString(),
      room: this.selectedRoom,
      interval: this.selectedInterval
    }
  }

  private runGetQuery(params: { start: string, end: string, room: string, interval: number }): void {
    this.webService.getQuery(
      params.start,
      params.end,
      params.room,
      params.interval
    ).subscribe({
      next: (data: any) => {
        this.queryResponse = data;
        if (this.queryResponse) {
          if (this.valueArray.length != 0) {
            this.valueArray = []
          }
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
        this.toggleLoadingAnimation()
        this.updateDataTable()
      },
      error: (error: any) => {
        this.showErrorToast('Error fetching data ' + error, 'Server Error')
        this.toggleLoadingAnimation()
      }
    })
  }


  onQueryButtonClick(): void {
    this.toggleLoadingAnimation()
    const params = this.getQueryParamsIfValid()
    if (params !== null) {
      this.queryResponse = null;
      this.runGetQuery(params)
    }
  }

  toggleLoadingAnimation(): void {
    this.loading = !this.loading;
  }

  onTimeIntervalChange(value: any): void {
    console.log("Time Interval:", value);
    this.removeOldData();
    this.selectedInterval = value;
  }

  onSensorChange(value: any): void {
    console.log("Sensor:", value);
    this.selectedSensor = value;
    if (this.queryResponse) {
      this.min = Infinity;
      this.max = -Infinity;
      this.updateMinAndMaxValuesFromData(this.queryResponse, this.getSelectedSensor());
      this.updateHeatmap();
      this.updateDataTable()
    }
  }

  getSliderValue(): string {
    return this.valueArray[this.sliderIndex];
  }

  onSliderChange(event: any) {
    this.sliderIndex = event.value;
    this.updateHeatmap()
    this.updateDataTable()
  }

  public getSelectedSensor(): string {
    return this.selectedSensor?.toLowerCase() ?? '';
  }

  private removeOldData(): void {
    if (this.queryResponse) {
      this.queryResponse = null;
      this.heatmapComponent?.removeHeatmapLayer();
    }
  }

  private updateHeatmap(): void {
    if (this.heatmapComponent) {
      this.heatmapComponent.removeHeatmapLayer()
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

  private showErrorToast(message: string, title?: string) {
    this.toasterService.danger(message, title, {
      limit: 3,
      duration: 3000,
      position: NbGlobalPhysicalPosition.BOTTOM_RIGHT,
      destroyByClick: true,
      preventDuplicates: true,
    })
  }

  roomData: { room_name: string, min: string, max: string, avg: string }[] = []


  private updateDataUnit(): void {
    switch (this.getSelectedSensor()) {
      case 'temperature':
        this.dataUnit = '°C'
        break;
      case 'humidity':
        this.dataUnit = '%'
        break;
      case 'co2':
        this.dataUnit = 'ppm'
        break;
      case 'light':
        this.dataUnit = 'lux'
        break;
      case 'pir':
        this.dataUnit = ''
        break;
      default:
        this.dataUnit = ''
    }
  }

  public updateDataTable(): void {
    if (this.queryResponse && this.getSliderValue()) {
      const newRoomData: { room_name: string, min: string, max: string, avg: string }[] = []
      const filteredData = this.queryResponse.filter((item: any) => {
        return this.rooms.includes(item['room_name']) && new Date(item['start']).getTime() === new Date(this.getSliderValue()).getTime()
      })
      this.updateDataUnit()
      filteredData.forEach((item: any) => {
        const sensors = item['sensors']
        sensors.filter((sensor: any) => sensor['type'] === this.getSelectedSensor()).forEach((s: any) => {
          newRoomData.push({
            room_name: item['room_name'],
            min: s['min'] + ' ' + this.dataUnit,
            max: s['max'] + ' ' + this.dataUnit,
            avg: s['mean'] + ' ' + this.dataUnit
          })
        })
      })
      this.roomData = newRoomData
    }
  }

}
