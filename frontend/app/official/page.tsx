'use client'

import { Download } from 'lucide-react'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { OfficialDashboardData } from '@/lib/types'

export default function OfficialDashboardPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [data, setData] = useState<OfficialDashboardData | null>(null)
  const [exporting, setExporting] = useState(false)

  useEffect(() => {
    api.get('/official/dashboard').then((r) => setData(r.data))
  }, [])

  const exportCsv = async () => {
    setExporting(true)
    try {
      const res = await api.get('/official/export', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const a = document.createElement('a')
      a.href = url
      a.download = 'farmalyze_district_surveillance.csv'
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } finally {
      setExporting(false)
    }
  }

  const s = data?.summary

  return (
    <AppShell
      eyebrow="Surveillance desk"
      title={<>State <i>surveillance.</i></>}
      roles={['official']}
      headerExtra={
        <button className="button button-dark" onClick={exportCsv} disabled={exporting} style={{ padding: '9px 14px' }}>
          <Download size={14} /> {exporting ? '…' : t(lang, 'exportCsv')}
        </button>
      }
    >
      {!data || !s ? (
        <p className="empty-state">Loading…</p>
      ) : (
        <>
          <div className="stat-grid">
            <div className="stat-card"><strong>{s.total_scans}</strong><span>{t(lang, 'totalScansStat')}</span></div>
            <div className="stat-card"><strong>{s.active_districts}</strong><span>{t(lang, 'activeDistricts')}</span></div>
            <div className="stat-card"><strong>{s.high_risk_zones}</strong><span>{t(lang, 'highRiskZones')}</span></div>
            <div className="stat-card"><strong>{s.pest_reports}</strong><span>{t(lang, 'pestReportsStat')}</span></div>
            <div className="stat-card"><strong>{s.confirmed_cases}</strong><span>{t(lang, 'confirmedCasesStat')}</span></div>
            <div className="stat-card"><strong>{s.registered_farmers}</strong><span>{t(lang, 'registeredFarmers')}</span></div>
          </div>

          <div className="grid-2" style={{ marginTop: 18 }}>
            <div className="panel-block" style={{ margin: 0 }}>
              <h2>{t(lang, 'topThreats')}</h2>
              {data.top_threats.length === 0 ? (
                <p className="empty-state">{t(lang, 'noDistrictData')}</p>
              ) : (
                <ul className="threat-list">
                  {data.top_threats.map((th) => (
                    <li key={`${th.name}-${th.kind}`}>
                      <span>
                        {th.name}
                        <em className={`kind-tag kind-${th.kind}`}>
                          {th.kind === 'pest' ? t(lang, 'pestLabel') : t(lang, 'diseaseLabel')}
                        </em>
                      </span>
                      <b>{th.districts} dist · {th.max_risk}</b>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="panel-block" style={{ margin: 0 }}>
              <h2>{t(lang, 'regionRollup')}</h2>
              <div style={{ overflowX: 'auto' }}>
                <table className="data-table">
                  <thead><tr><th>{t(lang, 'colRegion')}</th><th>Districts</th><th>{t(lang, 'highRiskZones')}</th><th>{t(lang, 'reports')}</th></tr></thead>
                  <tbody>
                    {data.regions.map((r) => (
                      <tr key={r.region}>
                        <td>{r.region}</td><td>{r.districts}</td><td>{r.high}</td><td>{r.reports}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="panel-block">
            <h2>{t(lang, 'districtTable')}</h2>
            <div style={{ overflowX: 'auto' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>{t(lang, 'colDistrict')}</th>
                    <th>{t(lang, 'colRegion')}</th>
                    <th>{t(lang, 'colScore')}</th>
                    <th>{t(lang, 'colForecast')}</th>
                    <th>{t(lang, 'colLevel')}</th>
                    <th>{t(lang, 'colThreat')}</th>
                    <th>{t(lang, 'colCropsAffected')}</th>
                    <th>{t(lang, 'colAction')}</th>
                  </tr>
                </thead>
                <tbody>
                  {data.districts.map((d) => (
                    <tr key={d.district}>
                      <td><b>{d.district}</b></td>
                      <td>{d.region}</td>
                      <td>{d.risk_score}</td>
                      <td>{typeof d.outbreak_forecast === 'number' ? `${d.outbreak_forecast}%` : '—'}</td>
                      <td><RiskBadge level={d.risk_level} lang={lang} /></td>
                      <td>
                        {d.dominant_threat || '—'}
                        {d.dominant_kind && (
                          <em className={`kind-tag kind-${d.dominant_kind}`}>
                            {d.dominant_kind === 'pest' ? t(lang, 'pestLabel') : t(lang, 'diseaseLabel')}
                          </em>
                        )}
                      </td>
                      <td>{d.crops_affected.join(', ') || '—'}</td>
                      <td style={{ fontSize: 12, color: 'var(--muted)', maxWidth: 260 }}>{d.recommended_action}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <p style={{ fontSize: 11, color: 'var(--muted)' }}>{data.note}</p>
        </>
      )}
    </AppShell>
  )
}
