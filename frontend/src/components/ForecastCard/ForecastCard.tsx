import type { SunsetForecast } from '../../types'
import { QualityMeter } from '../QualityMeter/QualityMeter'
import { SunsetDetails } from '../SunsetDetails/SunsetDetails'
import styles from './ForecastCard.module.css'

interface Props {
  forecast: SunsetForecast
  locationName?: string
}

export function ForecastCard({ forecast, locationName }: Props) {
  const displayName = locationName || forecast.location.name || `${forecast.location.lat.toFixed(3)}, ${forecast.location.lng.toFixed(3)}`

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div>
          <h2 className={styles.locationName}>{displayName}</h2>
          <p className={styles.date}>
            {new Date(forecast.forecast_date).toLocaleDateString(undefined, {
              weekday: 'long',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
      </div>

      <div className={styles.meterWrapper}>
        <QualityMeter score={forecast.quality_score} label={forecast.quality_label} />
      </div>

      <SunsetDetails forecast={forecast} />
    </div>
  )
}
