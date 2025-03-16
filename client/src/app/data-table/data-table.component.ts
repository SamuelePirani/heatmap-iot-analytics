import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
    selector: 'app-data-table',
    standalone: false,
    templateUrl: './data-table.component.html',
    styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent {
    @Input() roomData!: { room_name: string, min: number, max: number, avg: number }[];

    constructor() {
    }

    ngOnChanges(changes: SimpleChanges) {
        if (changes['roomData']) {
            this.roomData = changes['roomData'].currentValue;
        }
    }
}
