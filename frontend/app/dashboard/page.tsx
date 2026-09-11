'use client'

import { motion } from 'framer-motion'
import {
  Activity,
  ArrowUpRight,
  Camera,
  ChevronRight,
  CloudSun,
  Leaf,
  ShieldAlert,
  ShieldCheck,
  Sprout,
  Upload,
} from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useRef, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Alert, Crop, Hotspot, Prediction } from '@/lib/types'

const cropImage = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-QXMCNna5teLGPf6MRFl3i0e1iiPm2L.png'

export default function DashboardPage() {
  const { user } = useAuth()
  const router = useRouter()
  const fileRef = useRef<HTMLInputElement>(null)
  const [crops, setCrops] = useState<Crop[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [scans, setScans] = useState<Prediction[]>([])
  const [hotspots, setHotspots] = useState<Hotspot[]>([])
  const [activeCropId, setActiveCropId] = useState('')
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  const lang = user?.language || 'en'

  const load = () => {
    api.get('/crops').then((r) => {
      setCrops(r.data)
      if (r.data[0] && !activeCropId) setActiveCropId(r.data[0].id)
    })
    api.get('/alerts').then((r) => setAlerts(r.data.slice(0, 3)))
    api.get('/predictions').then((r) => setScans(r.data.slice(0, 5)))
    api.get('/risk-map').then((r) => setHotspots(r.data.hotspots?.slice(0, 3) || []))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const activeCrop = crops.find((c) => c.id === activeCropId) || crops[0]

  const stats = useMemo(() => {
    const total = scans.length
    const healthy = scans.filter((s) => s.disease.toLowerCase().includes('healthy')).length
    const resolved = scans.filter((s) => ['confirmed', 'corrected'].includes(s.verification_status)).length
    const healthyPct = total ? Math.round((healthy / total) * 100) : 0
    return { total, healthyPct, resolved }
  }, [scans])

  const hasHighRisk = crops.some((c) => c.current_risk?.level === 'high') || alerts.some((a) => a.severity === 'high')

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (!activeCrop) {
      setUploadError('Add a crop first before scanning.')
      return
    }
    setUploading(true)
    setUploadError('')
    const fd = new FormData()
    fd.append('file', file)
    fd.append('crop_id', activeCrop.id)
    fd.append('growth_stage', activeCrop.growth_stage)
    fd.append('district', activeCrop.district)
    fd.append('symptoms', '')
    try {
      const { data } = await api.post('/predict', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      router.push(`/prediction/${data.prediction_id}`)
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  const today = new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

  return (
    <AppShell eyebrow={today} title={<>{t(lang, 'goodDay')} <i>{user?.name?.split(' ')[0] || t(lang, 'there')}.</i></>} roles={['farmer']}>
      <motion.div
        className="status-banner"
        style={hasHighRisk ? { background: '#f6dfd6', borderLeftColor: '#a5432a' } : undefined}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="status-icon" style={hasHighRisk ? { color: '#a5432a' } : undefined}>
          {hasHighRisk ? <ShieldAlert size={22} /> : <ShieldCheck size={22} />}
        </div>
        <div>
          <strong>{hasHighRisk ? t(lang, 'fieldsAttention') : t(lang, 'fieldsStable')}</strong>
          <p>{hasHighRisk ? t(lang, 'highRiskDetected') : t(lang, 'noUrgentRisk')}</p>
        </div>
        <Link href="/alerts">{t(lang, 'viewAlerts')} <ArrowUpRight size={15} /></Link>
      </motion.div>

      <div className="dash-grid">
        <motion.section className="scan-panel" id="new-scan" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <div className="panel-label"><span>{t(lang, 'newDiagnosisLabel')}</span><Camera size={17} /></div>
          <h2>{t(lang, 'whatAreYouSeeing')}<br /><i>{t(lang, 'seeingToday')}</i></h2>
          <p>{t(lang, 'uploadCropCopy')}</p>
          {crops.length > 1 && (
            <div className="form-field" style={{ maxWidth: 320, marginTop: 20 }}>
              <label>{t(lang, 'scanningFor')}</label>
              <select value={activeCropId} onChange={(e) => setActiveCropId(e.target.value)}>
                {crops.map((c) => (
                  <option key={c.id} value={c.id}>{c.crop} — {c.district}</option>
                ))}
              </select>
            </div>
          )}
          {crops.length === 0 ? (
            <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 20 }}>
              <Link href="/crops" className="inline-link">{t(lang, 'addCropPrompt')}</Link> {t(lang, 'addCropSuffix')}
            </p>
          ) : (
            <label className="upload-zone">
              <input ref={fileRef} type="file" accept="image/*" onChange={onFile} disabled={uploading} />
              <span className="upload-symbol"><Upload size={22} /></span>
              <strong>{uploading ? t(lang, 'analyzing') : t(lang, 'dropLeafImage')}</strong>
              <small>{t(lang, 'uploadHint')}</small>
            </label>
          )}
          {uploadError && <p style={{ color: '#a5432a', fontSize: 12, marginTop: 10 }}>{uploadError}</p>}
        </motion.section>

        <motion.section className="field-panel" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <div className="panel-label"><span>{t(lang, 'fieldSnapshotLabel')}</span><CloudSun size={17} /></div>
          <div className="field-image">
            <img src={cropImage} alt="Green crop rows" />
            <span>{activeCrop ? activeCrop.district : t(lang, 'noFieldsYet')}</span>
          </div>
          <div className="field-meta">
            <div><small>{t(lang, 'currentCrop')}</small><strong>{activeCrop ? `${activeCrop.crop} · ${activeCrop.growth_stage}` : '—'}</strong></div>
            <div><small>{t(lang, 'currentRisk')}</small><strong>{activeCrop ? <RiskBadge level={activeCrop.current_risk?.level || 'low'} lang={lang} /> : '—'}</strong></div>
          </div>
          <Link className="arrow-link" href="/crops">{t(lang, 'manageFields')} <ChevronRight size={16} /></Link>
        </motion.section>
      </div>

      <section className="metrics-section">
        <div className="section-heading">
          <div>
            <p className="section-kicker">{t(lang, 'atAGlanceLabel')}</p>
            <h2>{t(lang, 'cropHealthFocus')} <i>{t(lang, 'inFocus')}</i></h2>
          </div>
          <Link className="arrow-link" href="/history">{t(lang, 'viewAllActivity')} <ChevronRight size={16} /></Link>
        </div>
        <div className="metric-row">
          <div><Leaf size={18} /><small>{t(lang, 'scansOnRecord')}</small><strong>{stats.total}</strong><span>{t(lang, 'acrossAllFields')}</span></div>
          <div><Sprout size={18} /><small>{t(lang, 'healthyCoverage')}</small><strong>{stats.healthyPct}%</strong><span className={stats.healthyPct >= 50 ? 'positive' : ''}>{t(lang, 'ofRecordedScans')}</span></div>
          <div><Activity size={18} /><small>{t(lang, 'issuesResolved')}</small><strong>{stats.resolved}</strong><span>{t(lang, 'confirmedByExpert')}</span></div>
        </div>
      </section>

      <div className="grid-2" style={{ marginTop: 30 }}>
        <div className="panel-block">
          <h2>{t(lang, 'recentAlerts')}</h2>
          {alerts.length === 0 ? (
            <p className="empty-state">{t(lang, 'noAlerts')}</p>
          ) : (
            <div style={{ display: 'grid', gap: 10 }}>
              {alerts.map((a) => (
                <div key={a.id} className={`alert-card severity-${a.severity}`}>
                  <RiskBadge level={a.severity} lang={lang} />
                  <p className="message">{a.message}</p>
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="panel-block">
          <h2>{t(lang, 'districtHotspots')}</h2>
          {hotspots.length === 0 ? (
            <p className="empty-state">{t(lang, 'noHotspotData')}</p>
          ) : (
            <div style={{ display: 'grid', gap: 10 }}>
              {hotspots.map((h) => (
                <div key={`${h.district}-${h.disease}`} className="hotspot-card" style={{ padding: '14px 16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <strong>{h.district}</strong>
                      <p className="disease" style={{ margin: '2px 0 0' }}>{h.disease}</p>
                    </div>
                    <RiskBadge level={h.risk_level} lang={lang} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {scans.length > 0 && (
        <div className="panel-block">
          <h2>{t(lang, 'recentScansTitle')}</h2>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr><th>{t(lang, 'colCrop')}</th><th>{t(lang, 'colDisease')}</th><th>{t(lang, 'colConfidence')}</th><th>{t(lang, 'colRisk')}</th></tr>
              </thead>
              <tbody>
                {scans.map((s) => (
                  <tr key={s.id}>
                    <td>{s.crop}</td>
                    <td><Link href={`/prediction/${s.id}`}>{s.disease}</Link></td>
                    <td>{(s.confidence * 100).toFixed(0)}%</td>
                    <td><RiskBadge level={s.risk?.level || 'low'} lang={lang} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </AppShell>
  )
}
