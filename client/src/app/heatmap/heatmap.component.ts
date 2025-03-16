import {Component, Inject, Input, OnChanges, PLATFORM_ID, SimpleChanges,} from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import VectorLayer from 'ol/layer/Vector';
import {Fill, Stroke, Style, Text} from 'ol/style';
import {Heatmap} from 'ol/layer';

@Component({
  selector: 'app-heatmap',
  standalone: false,
  templateUrl: './heatmap.component.html',
  styleUrls: ['./heatmap.component.scss'],
})
export class HeatmapComponent implements OnChanges {
  @Input() geoJsonUrl!: string;

  private map?: Map;
  private vectorSource?: VectorSource;

  constructor(@Inject(PLATFORM_ID) private readonly platformId: object) {
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['geoJsonUrl']) {
      if (this.map) {
        this.updateHeatmap();
      } else {
        this.initializeMap();
      }
    }
  }

  private normalizeValue(value: number, min: number, max: number): number {
    return (value - min) / (max - min)
  }

  public createHeatmap(data: any[], selectedSensor: string, startDate: string, min:number, max:number): void {
    const allFeatures = this.vectorSource?.getFeatures() ?? [];

    const pointSource = new VectorSource();

    const pointFeatures = allFeatures.filter((feature) => {
      if (feature && feature.getGeometry()) {
        return feature.getGeometry()?.getType() === 'Point';
      }
      return false;
    });

    pointFeatures.forEach((feature) => {
      const type = feature.get('type').split(' ')[0];
      if (type === selectedSensor) {
        const room = feature.get('room');
        const filteredData = data.filter((item) => {
          return room === item['room_name'] && new Date(item['start']).getTime() === new Date(startDate).getTime()
        })[0]
        let value = 0
        if (filteredData) {
          const sensors = filteredData['sensors']
          for (let i = 0; i < sensors.length; i++) {
            const sensorsData = sensors[i]
            if (sensorsData['type'] === selectedSensor) {
              value = sensorsData['mean']
            }
          }
        }
        feature.set('intensity', this.normalizeValue(value, min, max))
        pointSource.addFeature(feature.clone());
      }
    })

    const heatmapLayer = new Heatmap({
      source: pointSource,
      blur: 10,
      radius: 50,
      opacity: 0.80,
      weight: (feature) => feature.get('intensity') || 0
    })
    this.map?.addLayer(heatmapLayer)
  }

  private initializeMap(): void {
    this.vectorSource = new VectorSource({
      url: this.geoJsonUrl,
      format: new GeoJSON(),
    });

    const vectorLayer = this.createVectorLayer();

    this.map = new Map({
      target: 'heatmap',
      layers: [
        new TileLayer({source: new OSM()}),
        vectorLayer,
      ],
      view: new View({
        center: [0, 0],
        zoom: 2,
        minZoom: 19,
        maxZoom: 21,
      }),
    });

    this.vectorSource.once('change', () => {
      const features = this.vectorSource?.getFeatures() ?? [];
      if (features.length > 0) {
        // @ts-ignore
        const extent = this.vectorSource.getExtent();
        this.map?.getView().fit(extent, {
          padding: [20, 20, 20, 20],
          maxZoom: 21,
        });
      }
    });
  }

  private createVectorLayer(): VectorLayer {
    return new VectorLayer({
      source: this.vectorSource,
      style: (feature) => new Style({
        fill: new Fill({color: 'rgba(0,0,0,0.1)'}),
        stroke: new Stroke({
          color: '#000000',
          width: 2,
        }),
        text: new Text({
          text: feature.get('type') === 'Room' ? feature.get('name') || '' : '',
          font: '14px Arial',
          fill: new Fill({color: '#000'}),
          stroke: new Stroke({
            color: '#fff',
            width: 2,
          }),
        }),
      }),
    });
  }

  public removeHeatmapLayer(): void{
    console.log('Prima:', this.map?.getLayers().getArray());
    this.map?.getLayers().forEach((layer) => {
      if (layer instanceof Heatmap) {
        this.map?.removeLayer(layer);
      }
    });
    console.log('Dopo:', this.map?.getLayers().getArray());
  }


  private updateHeatmap(): void {
    this.vectorSource?.setUrl(this.geoJsonUrl);
    this.vectorSource?.refresh();
  }
}
