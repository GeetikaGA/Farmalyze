import { t } from '@/lib/i18n'
import type { Language, RiskLevel } from '@/lib/types'

export default function RiskBadge({ level, lang = 'en' }: { level: RiskLevel; lang?: Language }) {
  const cls = level === 'high' ? 'risk-high' : level === 'moderate' ? 'risk-moderate' : 'risk-low'
  const label = t(lang, level)
  return (
    <span className={`risk-badge ${cls}`}>
      <span aria-hidden>●</span> {label}
    </span>
  )
}
