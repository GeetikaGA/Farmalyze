'use client'

import { Bug, CheckCircle2, ShieldAlert } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Crop, MetaCrops, Pest, PestReportResult, RiskLevel } from '@/lib/types'

export default function ReportPestPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'

  const [pests, setPests] = useState<Pest[]>([])
  const [crops, setCrops] = useState<Crop[]>([])
  const [meta, setMeta] = useState<MetaCrops | null>(null)

  const [crop, setCrop] = useState('')
  const [district, setDistrict] = useState('')
  const [pestKey, setPestKey] = useState('')
  const [checked, setChecked] = useState<string[]>([])
  const [severity, setSeverity] = useState<RiskLevel>('moderate')
  const [notes, setNotes] = useState('')

  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<PestReportResult | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/meta/pests').then((r) => setPests(r.data.pests || []))
    api.get('/meta/crops').then((r) => setMeta(r.data))
    api.get('/crops').then((r) => {
      setCrops(r.data)
      if (r.data[0]) {
        setCrop(r.data[0].crop)
        setDistrict(r.data[0].district)
      }
    })
  }, [])

  // Crops offered = union of crops any pest covers (independent of the model's
  // trained crops, since pest reporting is a manual checklist, not image AI).
  const cropOptions = useMemo(() => {
    const set = new Set<string>()
    pests.forEach((p) => p.crops.forEach((c) => set.add(c)))
    crops.forEach((c) => set.add(c.crop))
    return Array.from(set).sort()
  }, [pests, crops])

  const availablePests = useMemo(
    () => pests.filter((p) => !crop || p.crops.some((c) => c.toLowerCase() === crop.toLowerCase())),
    [pests, crop],
  )
  const selectedPest = pests.find((p) => p.key === pestKey)

  const toggle = (sym: string) =>
    setChecked((prev) => (prev.includes(sym) ? prev.filter((s) => s !== sym) : [...prev, sym]))

  const districts = meta?.districts || []

  const submit = async () => {
    setError('')
    if (!crop || !district || !pestKey) {
      setError('Select a crop, district and pest first.')
      return
    }
    setSubmitting(true)
    try {
      const { data } = await api.post('/pest-report', {
        pest_key: pestKey,
        crop,
        district,
        observed_symptoms: checked,
        severity,
        notes: notes || null,
      })
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Submit failed')
    } finally {
      setSubmitting(false)
    }
  }

  const reset = () => {
    setResult(null)
    setChecked([])
    setNotes('')
    setSeverity('moderate')
  }

  if (result) {
    return (
      <AppShell eyebrow="Field report" title={<>Pest <i>report.</i></>} roles={['farmer']}>
        <div className="panel-block" style={{ borderLeft: '3px solid var(--green)' }}>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <CheckCircle2 className="status-icon" size={24} />
            <div>
              <h2 style={{ margin: 0 }}>{t(lang, 'pestReportSuccess')}</h2>
              <p style={{ color: 'var(--muted)', fontSize: 13, margin: '6px 0 0' }}>{t(lang, 'pestReportSuccessBody')}</p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 14, alignItems: 'center', marginTop: 18 }}>
            <RiskBadge level={result.risk.level} lang={lang} />
            <span className="hotspot-score">{result.pest} · {result.crop} · {result.district}</span>
          </div>
          {result.recommendation && (
            <div className="rec-columns" style={{ marginTop: 20 }}>
              <div>
                <h4>{t(lang, 'immediateActions')}</h4>
                <ul>{result.recommendation.immediate_actions.map((a, i) => <li key={i}>{a}</li>)}</ul>
              </div>
              <div>
                <h4>{t(lang, 'monitoring')}</h4>
                <ul>{result.recommendation.monitoring.map((a, i) => <li key={i}>{a}</li>)}</ul>
              </div>
              <div>
                <h4>{t(lang, 'preventive')}</h4>
                <ul>{result.recommendation.preventive_measures.map((a, i) => <li key={i}>{a}</li>)}</ul>
              </div>
            </div>
          )}
          <p className="disclaimer-note" style={{ marginTop: 18 }}>{t(lang, 'advisoryDisclaimer')}</p>
          <button className="button button-dark" onClick={reset}>{t(lang, 'reportAnother')}</button>
        </div>
      </AppShell>
    )
  }

  return (
    <AppShell eyebrow="Field report" title={<>Report a <i>pest.</i></>} roles={['farmer']}>
      <p className="panel-block" style={{ color: 'var(--muted)', fontSize: 13, lineHeight: 1.6, background: 'transparent', border: 0, padding: 0, marginBottom: 20, maxWidth: 640 }}>
        {t(lang, 'reportPestLede')}
      </p>

      <div className="diagnosis-grid">
        <div className="panel-block" style={{ margin: 0 }}>
          <div className="form-grid">
            <div className="form-field">
              <label>{t(lang, 'selectCropLabel')}</label>
              <select value={crop} onChange={(e) => { setCrop(e.target.value); setPestKey(''); setChecked([]) }}>
                <option value="">—</option>
                {cropOptions.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div className="form-field">
              <label>{t(lang, 'district')}</label>
              <select value={district} onChange={(e) => setDistrict(e.target.value)}>
                <option value="">—</option>
                {districts.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
          </div>

          <div className="form-field">
            <label>{t(lang, 'selectPestLabel')}</label>
            <select value={pestKey} onChange={(e) => { setPestKey(e.target.value); setChecked([]) }}>
              <option value="">—</option>
              {availablePests.map((p) => <option key={p.key} value={p.key}>{p.pest}</option>)}
            </select>
          </div>

          <div className="form-field">
            <label>{t(lang, 'severityLabel')}</label>
            <select value={severity} onChange={(e) => setSeverity(e.target.value as RiskLevel)}>
              <option value="low">{t(lang, 'low')}</option>
              <option value="moderate">{t(lang, 'moderate')}</option>
              <option value="high">{t(lang, 'high')}</option>
            </select>
          </div>

          <div className="form-field">
            <label>{t(lang, 'addNotesLabel')}</label>
            <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} placeholder={t(lang, 'addNotesPlaceholder')} />
          </div>

          {error && <p style={{ color: '#a5432a', fontSize: 12 }}>{error}</p>}
          <button className="button button-dark button-block" onClick={submit} disabled={submitting}>
            <Bug size={15} /> {submitting ? t(lang, 'submittingReport') : t(lang, 'submitPestReport')}
          </button>
          <p className="disclaimer-note" style={{ marginTop: 14 }}>{t(lang, 'pestMethodNote')}</p>
        </div>

        <div className="panel-block" style={{ margin: 0 }}>
          <h2 style={{ fontSize: 26 }}>{t(lang, 'observedSymptoms')}</h2>
          {!selectedPest ? (
            <p className="empty-state">{t(lang, 'selectPestFirst')}</p>
          ) : (
            <>
              <p style={{ color: 'var(--muted)', fontSize: 12, marginBottom: 14 }}>{t(lang, 'checklistPrompt')}</p>
              <div className="checklist">
                {selectedPest.checklist.map((sym) => (
                  <label key={sym} className={checked.includes(sym) ? 'checklist-item checked' : 'checklist-item'}>
                    <input type="checkbox" checked={checked.includes(sym)} onChange={() => toggle(sym)} />
                    <span>{sym}</span>
                  </label>
                ))}
              </div>
              <div className="checklist-note">
                <ShieldAlert size={15} />
                <span>{selectedPest.symptoms}</span>
              </div>
            </>
          )}
        </div>
      </div>
    </AppShell>
  )
}
