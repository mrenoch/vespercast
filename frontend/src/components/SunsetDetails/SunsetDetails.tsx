import { format } from 'date-fns'
import { toZonedTime } from 'date-fns-tz'
import type { SunsetForecast } from '../../types'
import styles from './SunsetDetails.module.css'

interface Props {
  forecast: SunsetForecast
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className={styles.detail}>
      <span className={styles.detailLabel}>{label}</span>
      <span className={styles.detailValue}>{value}</span>
    </div>
  )
}

function formatUtcTime(isoString: string): string {
  try {
    return format(new Date(isoString), 'h:mm a zzz')
  } catch {
    return isoString
  }
}

export function SunsetDetails({ forecast }: Props) {
  return (
    <div className={styles.container}>
      <h3 className={styles.heading}>Conditions at Sunset</h3>
      <div className={styles.grid}>
        <Detail label="Sunset" value={formatUtcTime(forecast.sunset_time_utc)} />
        <Detail label="Golden Hour" value={formatUtcTime(forecast.golden_hour_start_utc)} />
        <Detail label="Cloud Cover" value={`${forecast.cloud_cover_total.toFixed(0)}%`} />
        <Detail label="Low Clouds" value={`${forecast.cloud_cover_low.toFixed(0)}%`} />
        <Detail label="Mid Clouds" value={`${forecast.cloud_cover_mid.toFixed(0)}%`} />
        <Detail label="High Clouds" value={`${forecast.cloud_cover_high.toFixed(0)}%`} />
        <Detail label="Humidity" value={`${forecast.relative_humidity.toFixed(0)}%`} />
        <Detail label="Precip Prob" value={`${forecast.precipitation_probability.toFixed(0)}%`} />
        <Detail
          label="Precipitation"
          value={forecast.precipitation > 0 ? `${forecast.precipitation.toFixed(1)} mm` : 'None'}
        />
        <Detail
          label="Visibility"
          value={forecast.visibility !== null ? `${forecast.visibility.toFixed(0)} km` : 'Unknown'}
        />
        <Detail
          label="Wind"
          value={forecast.wind_speed !== null ? `${forecast.wind_speed.toFixed(0)} km/h` : 'Unknown'}
        />
      </div>
    </div>
  )
}
