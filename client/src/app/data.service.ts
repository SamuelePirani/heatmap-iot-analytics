import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class DataService {
    private baseUrl = 'http://localhost:5000';

    constructor(private http: HttpClient) {
    }

    getData(room?: string, start?: string, end?: string, sensor?: string): Observable<any> {
        let params = new HttpParams();
        if (room) {
            params = params.set('room', room);
        }
        if (start) {
            params = params.set('start', start);
        }
        if (end) {
            params = params.set('end', end);
        }
        if (sensor) {
            params = params.set('sensor', sensor);
        }

        return this.http.get<any>(`${this.baseUrl}/api/data`, {params});
    }
}