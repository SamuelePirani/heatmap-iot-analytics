import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
    selector: 'app-data-table',
    standalone: false,
    templateUrl: './data-table.component.html',
    styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent {
    @Input() min!: number;
    @Input() max!: number;
    @Input() roomData!: { room_name: string, min: number, max: number, avg: number }[];

    constructor() {
        this.roomData = [
            { room_name: 'room1', min: this.getRandomNumber(10, 20), max: this.getRandomNumber(30, 40), avg: this.getRandomNumber(15, 35) },
            { room_name: 'room2', min: this.getRandomNumber(5, 15), max: this.getRandomNumber(25, 35), avg: this.getRandomNumber(12, 30) },
            { room_name: 'room3', min: this.getRandomNumber(20, 30), max: this.getRandomNumber(40, 50), avg: this.getRandomNumber(25, 45) },
            { room_name: 'room4', min: this.getRandomNumber(0, 10), max: this.getRandomNumber(20, 30), avg: this.getRandomNumber(5, 20) }
        ]
    }

    getRandomNumber(min: number, max: number): number {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
}
