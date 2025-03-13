import {Component, Inject, Input, PLATFORM_ID} from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import VectorLayer from 'ol/layer/Vector';
import {Fill, Stroke, Style, Text} from 'ol/style';

@Component({
    selector: 'app-heatmap',
    standalone: false,
    templateUrl: './heatmap.component.html',
    styleUrl: './heatmap.component.scss'
})
export class HeatmapComponent {
    @Input() geoJsonUrl!: string;
    map!: Map;
    vectorSource!: VectorSource;

    constructor(@Inject(PLATFORM_ID) private platformId: Object) {
    }

    ngOnChanges(): void {
        if (this.map) {
            this.updateHeatmap();
        } else {
            this.initializeMap();
        }
    }

    initializeMap(): void {
        this.vectorSource = new VectorSource({
            url: this.geoJsonUrl,
            format: new GeoJSON(),
        });

        const vectorLayer = this.layoutCreation();

        this.map = new Map({
            target: 'heatmap',
            layers: [
                new TileLayer({
                    source: new OSM(),
                }),
                vectorLayer
            ],
            view: new View({
                center: [0, 0],
                zoom: 2,
            }),
        });


        this.vectorSource.once('change', () => {
            if (this.vectorSource.getFeatures().length > 0) {
                const extent = this.vectorSource.getExtent();
                this.map.getView().fit(extent, {padding: [20, 20, 20, 20], maxZoom: 20});
            }
        });
    }

    layoutCreation(): VectorLayer {
        return new VectorLayer({
            source: this.vectorSource,
            style: (feature) => {
                return new Style({
                    fill: new Fill({
                        color: 'rgba(0,0,0,0.1)',
                    }),
                    stroke: new Stroke({
                        color: '#000000',
                        width: 2,
                    }),
                    text: new Text({
                        text: feature.get('type') === 'Room' ? feature.get('name') : '',
                        font: '14px Arial',
                        fill: new Fill({
                            color: '#000',
                        }),
                        stroke: new Stroke({
                            color: '#fff',
                            width: 2,
                        }),
                    }),
                });
            },
        });
    }


    updateHeatmap(): void {
        this.vectorSource.setUrl(this.geoJsonUrl);
        this.vectorSource.refresh();
    }
}
