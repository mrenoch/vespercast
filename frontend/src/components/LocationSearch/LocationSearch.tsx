import { useState } from 'react'
import { geocodeAddress } from '../../api/client'
import type { GeocodeResult } from '../../types'
import styles from './LocationSearch.module.css'

interface Props {
  onLocationSelected: (result: GeocodeResult) => void
}

export function LocationSearch({ onLocationSelected }: Props) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    try {
      const result = await geocodeAddress(query)
      onLocationSelected(result)
    } catch {
      setError('Location not found. Try a more specific address.')
    } finally {
      setLoading(false)
    }
  }

  function handleGeolocate() {
    if (!navigator.geolocation) {
      setError('Geolocation not supported by your browser.')
      return
    }
    setLoading(true)
    setError(null)
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        onLocationSelected({
          name: 'Current location',
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          elevation: pos.coords.altitude,
        })
        setLoading(false)
      },
      () => {
        setError('Could not get your location.')
        setLoading(false)
      },
    )
  }

  return (
    <div className={styles.container}>
      <form onSubmit={handleSearch} className={styles.form}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a city, address, or landmark..."
          className={styles.input}
          disabled={loading}
        />
        <button type="submit" className={styles.searchBtn} disabled={loading || !query.trim()}>
          {loading ? 'Searching…' : 'Search'}
        </button>
        <button type="button" onClick={handleGeolocate} className={styles.geoBtn} disabled={loading}>
          📍 Use my location
        </button>
      </form>
      {error && <p className={styles.error}>{error}</p>}
    </div>
  )
}
