import styles from './QualityMeter.module.css'

interface Props {
  score: number
  label: string
}

const LABEL_COLORS: Record<string, string> = {
  poor: '#94a3b8',
  fair: '#fbbf24',
  good: '#34d399',
  great: '#f97316',
  epic: '#a855f7',
}

export function QualityMeter({ score, label }: Props) {
  const color = LABEL_COLORS[label] ?? '#f97316'
  const pct = Math.min(100, Math.max(0, score))

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <span className={styles.label} style={{ color }}>
          {label.toUpperCase()}
        </span>
        <span className={styles.score}>{score.toFixed(0)}/100</span>
      </div>
      <div className={styles.track}>
        <div
          className={styles.fill}
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  )
}
