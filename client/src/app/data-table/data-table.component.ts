import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
    selector: 'app-data-table',
    standalone: false,
    templateUrl: './data-table.component.html',
    styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent {
    @Input() roomData!: { room_name: string, min: string, max: string, avg: string }[];

    constructor() {
    }

    ngOnChanges(changes: SimpleChanges) {
        if (changes['roomData']) {
            this.roomData = changes['roomData'].currentValue;
        }
    }
}
