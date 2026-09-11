'use client'

import { Plus } from 'lucide-react'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Crop, MetaCrops } from '@/lib/types'

export default function CropsPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [crops, setCrops] = useState<Crop[]>([])
  const [meta, setMeta] = useState<MetaCrops>({ crops: [], growth_stages: {}, districts: [] })
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ crop: '', variety: '', growth_stage: '', district: '' })

  const load = () => api.get('/crops').then((r) => setCrops(r.data))

  useEffect(() => {
    load()
    api.get('/meta/crops').then((r) => {
      setMeta(r.data)
      const firstCrop = r.data.crops[0]
      setForm({
        crop: firstCrop || '',
        variety: '',
        growth_stage: r.data.growth_stages[firstCrop]?.[0] || '',
        district: r.data.districts[0] || '',
      })
    })
  }, [])

  const stages = meta.growth_stages[form.crop] || []

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post('/crops', form)
      setShowForm(false)
      load()
    } finally {
      setSaving(false)
    }
  }

  return (
    <AppShell eyebrow="Field workspace" title={<>My <i>crops.</i></>} roles={['farmer']}>
      <div className="page-head">
        <div />
        <button className="button button-dark" onClick={() => setShowForm(!showForm)}>
          <Plus size={16} /> Add crop
        </button>
      </div>

      {showForm && (
        <form onSubmit={submit} className="panel-block form-grid" style={{ marginBottom: 24 }}>
          <div className="form-field">
            <label>Crop</label>
            <select
              value={form.crop}
              onChange={(e) => setForm({ ...form, crop: e.target.value, growth_stage: meta.growth_stages[e.target.value]?.[0] || '' })}
            >
              {meta.crops.map((c) => <option key={c}>{c}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Variety (optional)</label>
            <input value={form.variety} onChange={(e) => setForm({ ...form, variety: e.target.value })} placeholder="e.g. Hybrid, Desi" />
          </div>
          <div className="form-field">
            <label>Growth stage</label>
            <select value={form.growth_stage} onChange={(e) => setForm({ ...form, growth_stage: e.target.value })}>
              {stages.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>District</label>
            <select value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })}>
              {meta.districts.map((d) => <option key={d}>{d}</option>)}
            </select>
          </div>
          <button type="submit" className="button button-dark" style={{ gridColumn: '1 / -1' }} disabled={saving}>
            {saving ? 'Saving…' : 'Save crop'}
          </button>
        </form>
      )}

      {crops.length === 0 ? (
        <p className="empty-state">No crops yet. Add your first field above to start scanning.</p>
      ) : (
        <div className="grid-2">
          {crops.map((c) => (
            <Link key={c.id} href={`/crops/${c.id}`} className="crop-card">
              <div className="crop-card-top">
                <h3>{c.crop}</h3>
                <RiskBadge level={c.current_risk?.level || 'low'} lang={lang} />
              </div>
              <p>{c.variety || '—'} · {c.growth_stage}</p>
              <p>{c.district} · Risk {c.current_risk?.score ?? 0}/100</p>
              <span className={`kind-tag ${(meta.crop_capability?.[c.crop] || 'ai_disease') === 'ai_disease' ? 'kind-disease' : 'kind-pest'}`} style={{ marginLeft: 0, marginTop: 10, display: 'inline-block' }}>
                {(meta.crop_capability?.[c.crop] || 'ai_disease') === 'ai_disease' ? t(lang, 'capAi') : t(lang, 'capAdvisory')}
              </span>
            </Link>
          ))}
        </div>
      )}
    </AppShell>
  )
}
