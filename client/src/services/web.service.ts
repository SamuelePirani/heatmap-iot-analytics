import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebService {

  private apiUrl = 'http://localhost:5000/';

  constructor(private http: HttpClient) {
  }

  getRange(): Observable<any> {
    return this.http.get(this.apiUrl + 'range');
  }

  getQuery(start: string, end: string, room: string | null, sensor: string, interval: number): Observable<any> {
    const isoStart = new Date(start).toISOString();
    const isoEnd = new Date(end).toISOString();
    const params = new HttpParams()
      .set('start', isoStart)
      .set('end', isoEnd)
      .set('room_name', room || '')
      .set('interval', interval.toString());
    return this.http.get(this.apiUrl + '/data_room', {params})
  }
}
