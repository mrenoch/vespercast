import axios from 'axios'
import type { SunsetForecast, GeocodeResult, ForecastParams } from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export async function geocodeAddress(address: string): Promise<GeocodeResult> {
  const { data } = await api.post<GeocodeResult>('/locations/geocode/', { address })
  return data
}

export async function getForecast(params: ForecastParams): Promise<SunsetForecast> {
  const { data } = await api.get<SunsetForecast>('/forecasts/', { params })
  return data
}

export async function submitRating(forecastId: number, score: number, comment = ''): Promise<void> {
  await api.post('/ratings/', { forecast: forecastId, score, comment })
}

export async function saveLocation(lat: number, lng: number, name: string, elevation?: number | null) {
  const { data } = await api.post('/locations/', { lat, lng, name, elevation })
  return data
}
