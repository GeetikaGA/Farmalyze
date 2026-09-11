'use client'

import dynamic from 'next/dynamic'
import { List, Map as MapIcon } from 'lucide-react'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { DistrictRisk, Hotspot } from '@/lib/types'

const MaharashtraRiskMap = dynamic(() => import('@/components/MaharashtraRiskMap'), {
  ssr: false,
  loading: () => <div className="mh-map mh-map-loading">Loading map…</div>,
})

export default function RiskMapPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [districts, setDistricts] = useState<DistrictRisk[]>([])
  const [hotspots, setHotspots] = useState<Hotspot[]>([])
  const [note, setNote] = useState('')
  const [view, setView] = useState<'map' | 'list'>('map')
  const [selected, setSelected] = useState<DistrictRisk | null>(null)

  useEffect(() => {
    api.get('/risk-map').then((r) => {
      setDistricts(r.data.districts || [])
      setHotspots(r.data.hotspots || [])
      setNote(r.data.note || '')
    })
  }, [])

  return (
    <AppShell
      eyebrow="District intelligence"
      title={<>Risk <i>map.</i></>}
      headerExtra={
        <div className="seg-toggle">
          <button className={view === 'map' ? 'active' : ''} onClick={() => setView('map')}>
            <MapIcon size={14} /> {t(lang, 'mapViewMap')}
          </button>
          <button className={view === 'list' ? 'active' : ''} onClick={() => setView('list')}>
            <List size={14} /> {t(lang, 'mapViewList')}
          </button>
        </div>
      }
    >
      <p style={{ color: 'var(--muted)', fontSize: 12, marginBottom: 16, maxWidth: 620 }}>{note}</p>

      {view === 'map' ? (
        <div className="map-layout">
          <div>
            <MaharashtraRiskMap districts={districts} onSelect={setSelected} />
            <div className="map-legend">
              <span>{t(lang, 'mapLegend')}:</span>
              <em><i className="lg lg-high" /> {t(lang, 'high')}</em>
              <em><i className="lg lg-moderate" /> {t(lang, 'moderate')}</em>
              <em><i className="lg lg-low" /> {t(lang, 'low')}</em>
              <em><i className="lg lg-none" /> —</em>
            </div>
            <p style={{ color: 'var(--muted)', fontSize: 11, marginTop: 10 }}>{t(lang, 'clickDistrictHint')}</p>
          </div>

          <aside className="map-detail">
            {!selected ? (
              <p className="empty-state">{t(lang, 'clickDistrictHint')}</p>
            ) : (
              <div className="panel-block" style={{ margin: 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h2 style={{ margin: 0 }}>{selected.district}</h2>
                  <RiskBadge level={selected.risk_level} lang={lang} />
                </div>
                <p className="disease" style={{ color: 'var(--muted)', fontSize: 12, margin: '6px 0 16px' }}>
                  {selected.region} · {selected.risk_score}/100
                </p>

                {typeof selected.outbreak_forecast === 'number' && (
                  <>
                    <h4 className="detail-h">{t(lang, 'predictedOutbreak')}</h4>
                    <div className="forecast-meter">
                      <div className="forecast-num">
                        <strong>{selected.outbreak_forecast}%</strong>
                        {selected.forecast_level && <RiskBadge level={selected.forecast_level} lang={lang} />}
                      </div>
                      <div className="forecast-bar">
                        <span
                          className={`forecast-fill fill-${selected.forecast_level || 'low'}`}
                          style={{ width: `${selected.outbreak_forecast}%` }}
                        />
                      </div>
                    </div>
                  </>
                )}

                <h4 className="detail-h">{t(lang, 'threatsDetected')}</h4>
                <ul className="threat-list">
                  {selected.threats.map((th) => (
                    <li key={th.name}>
                      <span>
                        <i className={`dot dot-${th.risk_level}`} /> {th.name}
                        <em className={`kind-tag kind-${th.kind}`}>
                          {th.kind === 'pest' ? t(lang, 'pestLabel') : t(lang, 'diseaseLabel')}
                        </em>
                      </span>
                      <b>{th.risk_score}</b>
                    </li>
                  ))}
                </ul>

                <h4 className="detail-h">{t(lang, 'cropsAffected')}</h4>
                <p style={{ fontSize: 13 }}>{selected.crops_affected.join(', ') || '—'}</p>

                <h4 className="detail-h">{t(lang, 'recommendedAction')}</h4>
                <p className="action-box">{selected.recommended_action}</p>
              </div>
            )}
          </aside>
        </div>
      ) : (
        <>
          {hotspots.length === 0 ? (
            <p className="empty-state">{t(lang, 'noDistrictData')}</p>
          ) : (
            <div className="grid-3">
              {hotspots.map((h) => (
                <div key={`${h.district}-${h.disease}`} className="hotspot-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h3>{h.district}</h3>
                    <span className={`kind-tag kind-${h.kind || 'disease'}`}>
                      {h.kind === 'pest' ? t(lang, 'pestLabel') : t(lang, 'diseaseLabel')}
                    </span>
                  </div>
                  <p className="disease">{h.disease}</p>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <RiskBadge level={h.risk_level} lang={lang} />
                    <span className="hotspot-score">{h.risk_score}/100</span>
                  </div>
                  <dl>
                    <div><span>{t(lang, 'reports')}</span><dd>{h.report_count}</dd></div>
                    <div><span>{t(lang, 'trend')}</span><dd style={{ textTransform: 'capitalize' }}>{h.trend}</dd></div>
                  </dl>
                  {h.demo && <p className="demo-tag">Demo/simulated aggregate</p>}
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </AppShell>
  )
}
