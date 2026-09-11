'use client'

import { ShieldQuestion } from 'lucide-react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api, { mediaUrl } from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Prediction } from '@/lib/types'

export default function PredictionPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [pred, setPred] = useState<Prediction | null>(null)
  const [verifyMsg, setVerifyMsg] = useState('')

  const load = () => api.get(`/predictions/${id}`).then((r) => setPred(r.data))

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const requestVerify = async () => {
    await api.post('/verify-request', { prediction_id: id })
    setVerifyMsg('Verification request submitted.')
    load()
  }

  if (!pred) {
    return (
      <AppShell eyebrow="Diagnosis" title="Loading…">
        <p className="empty-state">Loading…</p>
      </AppShell>
    )
  }

  const confPct = (pred.confidence * 100).toFixed(1)

  return (
    <AppShell eyebrow="Diagnosis result" title={<>{pred.disease}</>}>
      {pred.capability === 'advisory_pest' ? (
        <div className="status-banner" style={{ background: '#eef1fb', borderLeftColor: '#5b4b8a', marginBottom: 16 }}>
          <div className="status-icon" style={{ color: '#5b4b8a' }}><ShieldQuestion size={22} /></div>
          <div>
            <strong>{t(lang, 'aiComingSoonTitle')}</strong>
            <p>{t(lang, 'aiComingSoonBody')}</p>
          </div>
          <Link href="/report-pest" style={{ marginLeft: 'auto', fontSize: 11, fontWeight: 700 }}>{t(lang, 'navReportPest')} →</Link>
        </div>
      ) : (
        <p className="disclaimer-note">{t(lang, 'aiDisclaimer')}</p>
      )}

      <div className="diagnosis-grid">
        <div className="panel-block">
          {pred.image_url && <img src={mediaUrl(pred.image_url)} alt="Scanned crop" className="diagnosis-image" />}
          <h2 style={{ fontSize: 26 }}>{pred.disease}</h2>
          <p style={{ color: 'var(--muted)', fontSize: 13, margin: '4px 0 14px' }}>{pred.crop} · {pred.district}</p>
          <p style={{ fontSize: 13 }}><strong>{t(lang, 'confidence')}:</strong> {confPct}% ({pred.confidence_level})</p>
          {pred.confidence_level === 'low' && (
            <p style={{ color: '#8a6d16', fontSize: 12, marginTop: 8 }}>Low confidence — expert verification strongly recommended.</p>
          )}
          {pred.confidence_level === 'medium' && (
            <p style={{ color: '#8a6d16', fontSize: 12, marginTop: 8 }}>Moderate confidence — monitor closely and consider verification.</p>
          )}
          <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 10 }}>{t(lang, 'verificationStatus')}: <strong style={{ color: 'var(--ink)', textTransform: 'capitalize' }}>{pred.verification?.status || pred.verification_status}</strong></p>
        </div>

        <div style={{ display: 'grid', gap: 18 }}>
          <div className="panel-block" style={{ marginBottom: 0 }}>
            <h2 style={{ fontSize: 18 }}>{t(lang, 'whyPrediction')}</h2>
            {pred.explanation?.available && pred.explanation?.heatmap_url ? (
              <img src={mediaUrl(pred.explanation.heatmap_url)} alt="Grad-CAM heatmap" className="diagnosis-image heatmap" style={{ marginTop: 10 }} />
            ) : (
              <p style={{ fontSize: 13, color: 'var(--muted)', marginTop: 8 }}>{pred.explanation?.message || 'Explainability not available for this scan.'}</p>
            )}
          </div>

          <div className="panel-block" style={{ marginBottom: 0 }}>
            <h2 style={{ fontSize: 18 }}>{t(lang, 'riskScore')}: {pred.risk?.score}/100</h2>
            <div style={{ marginTop: 8 }}><RiskBadge level={pred.risk?.level || 'low'} lang={lang} /></div>
            <p style={{ fontSize: 13, color: 'var(--muted)', marginTop: 10 }}>{pred.risk?.explanation}</p>
            <h4 style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '.05em', color: 'var(--green)', marginTop: 16 }}>{t(lang, 'riskFactors')}</h4>
            <ul className="risk-factor-list">
              {pred.risk?.factors?.map((f) => (
                <li key={f.name}><span>{f.name}</span><strong style={{ textTransform: 'capitalize' }}>{f.level}</strong></li>
              ))}
            </ul>
          </div>

          {pred.forecast && (
            <div className="panel-block" style={{ marginBottom: 0 }}>
              <h2 style={{ fontSize: 18 }}>{t(lang, 'predictedOutbreak')}</h2>
              <div className="forecast-meter">
                <div className="forecast-num">
                  <strong>{pred.forecast.probability}%</strong>
                  <RiskBadge level={pred.forecast.level} lang={lang} />
                </div>
                <div className="forecast-bar">
                  <span className={`forecast-fill fill-${pred.forecast.level}`} style={{ width: `${pred.forecast.probability}%` }} />
                </div>
              </div>
              <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 10 }}>{t(lang, 'outbreakForecastNote')}</p>
            </div>
          )}
        </div>

        <div className="panel-block" style={{ gridColumn: '1 / -1' }}>
          <h2 style={{ fontSize: 20 }}>{pred.recommendation?.title}</h2>
          <p className="disclaimer-note">{t(lang, 'advisoryDisclaimer')}</p>
          <div className="rec-columns">
            <div>
              <h4>{t(lang, 'immediateActions')}</h4>
              <ul>{pred.recommendation?.immediate_actions?.map((a) => <li key={a}>{a}</li>)}</ul>
            </div>
            <div>
              <h4>{t(lang, 'monitoring')}</h4>
              <ul>{pred.recommendation?.monitoring?.map((a) => <li key={a}>{a}</li>)}</ul>
            </div>
            <div>
              <h4>{t(lang, 'preventive')}</h4>
              <ul>{pred.recommendation?.preventive_measures?.map((a) => <li key={a}>{a}</li>)}</ul>
            </div>
          </div>
          {(pred.verification?.recommended || pred.confidence_level !== 'high') && pred.verification_status !== 'pending' && (
            <button onClick={requestVerify} className="button button-outline" style={{ marginTop: 20 }}>
              <ShieldQuestion size={16} /> {t(lang, 'requestVerification')}
            </button>
          )}
          {verifyMsg && <p style={{ color: 'var(--green)', fontSize: 12, marginTop: 10 }}>{verifyMsg}</p>}
        </div>
      </div>
    </AppShell>
  )
}
