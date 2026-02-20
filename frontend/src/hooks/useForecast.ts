import { useQuery } from '@tanstack/react-query'
import { getForecast } from '../api/client'
import type { ForecastParams, SunsetForecast } from '../types'

export function useForecast(params: ForecastParams | null) {
  return useQuery<SunsetForecast, Error>({
    queryKey: ['forecast', params],
    queryFn: () => getForecast(params!),
    enabled: params !== null,
    staleTime: 3 * 60 * 60 * 1000, // 3 hours — matches backend cache
    retry: 1,
  })
}
