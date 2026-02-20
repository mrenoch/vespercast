import { useState } from 'react'
import { LocationSearch } from '../components/LocationSearch/LocationSearch'
import { ForecastCard } from '../components/ForecastCard/ForecastCard'
import { useForecast } from '../hooks/useForecast'
import type { ForecastParams, GeocodeResult } from '../types'
import styles from './HomePage.module.css'

export function HomePage() {
  const [geocodeResult, setGeocodeResult] = useState<GeocodeResult | null>(null)
  const [forecastParams, setForecastParams] = useState<ForecastParams | null>(null)

  const { data: forecast, isLoading, error } = useForecast(forecastParams)

  function handleLocationSelected(result: GeocodeResult) {
    setGeocodeResult(result)
    setForecastParams({ lat: result.lat, lng: result.lng })
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>VesperCast</h1>
        <p className={styles.subtitle}>Sunset quality forecasts for your favorite spots</p>
      </header>

      <main className={styles.main}>
        <LocationSearch onLocationSelected={handleLocationSelected} />

        <div className={styles.result}>
          {isLoading && (
            <div className={styles.loading}>
              <div className={styles.spinner} />
              <p>Calculating sunset quality…</p>
            </div>
          )}

          {error && (
            <div className={styles.errorCard}>
              <p>Could not load forecast: {error.message}</p>
            </div>
          )}

          {forecast && !isLoading && (
            <ForecastCard
              forecast={forecast}
              locationName={geocodeResult?.name}
            />
          )}

          {!forecast && !isLoading && !error && (
            <div className={styles.empty}>
              <p>Enter a location above to see today's sunset forecast</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
