import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebService {

  private apiUrl = 'http://localhost:5000/range';

  constructor(private http: HttpClient) { }

  getRange(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}
