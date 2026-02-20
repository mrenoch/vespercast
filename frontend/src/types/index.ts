export interface Location {
  id: number
  name: string
  lat: number
  lng: number
  elevation: number | null
  horizon_elevation_west: number
  created_at: string
}

export interface SunsetForecast {
  id: number
  location: Location
  forecast_date: string
  sunset_time_utc: string
  golden_hour_start_utc: string
  cloud_cover_total: number
  cloud_cover_low: number
  cloud_cover_mid: number
  cloud_cover_high: number
  relative_humidity: number
  precipitation_probability: number
  precipitation: number
  visibility: number | null
  wind_speed: number | null
  quality_score: number
  quality_label: 'poor' | 'fair' | 'good' | 'great' | 'epic'
  fetched_at: string
}

export interface GeocodeResult {
  name: string
  lat: number
  lng: number
  elevation: number | null
}

export interface ForecastParams {
  lat: number
  lng: number
  date?: string
}
