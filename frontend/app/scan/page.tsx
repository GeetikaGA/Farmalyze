'use client'

import { ArrowRight, Upload } from 'lucide-react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { Suspense, useEffect, useRef, useState } from 'react'
import AppShell from '@/components/AppShell'
import api from '@/lib/api'
import type { Crop, MetaCrops } from '@/lib/types'

export default function ScanPage() {
  return (
    <Suspense fallback={null}>
      <ScanPageInner />
    </Suspense>
  )
}

function ScanPageInner() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const fileRef = useRef<HTMLInputElement>(null)
  const [crops, setCrops] = useState<Crop[]>([])
  const [meta, setMeta] = useState<MetaCrops>({ crops: [], growth_stages: {}, districts: [] })
  const [form, setForm] = useState({ crop_id: '', growth_stage: '', district: '', symptoms: '' })
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/crops').then((r) => {
      setCrops(r.data)
      const preselect = searchParams.get('crop_id')
      const match = r.data.find((c: Crop) => c.id === preselect) || r.data[0]
      if (match) {
        setForm((f) => ({ ...f, crop_id: match.id, growth_stage: match.growth_stage, district: match.district }))
      }
    })
    api.get('/meta/crops').then((r) => setMeta(r.data))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const selectedCrop = crops.find((c) => c.id === form.crop_id)
  const stages = selectedCrop ? meta.growth_stages[selectedCrop.crop] || [] : []
  const capability = selectedCrop ? meta.crop_capability?.[selectedCrop.crop] || 'ai_disease' : 'ai_disease'
  const aiCrop = capability === 'ai_disease'

  const onFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
  }

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('Please select an image')
      return
    }
    setLoading(true)
    setError('')
    const fd = new FormData()
    fd.append('file', file)
    fd.append('crop_id', form.crop_id)
    fd.append('growth_stage', form.growth_stage)
    fd.append('district', form.district)
    fd.append('symptoms', form.symptoms)
    try {
      const { data } = await api.post('/predict', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      router.push(`/prediction/${data.prediction_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppShell eyebrow="New diagnosis" title={<>Scan a <i>crop.</i></>} roles={['farmer']}>
      {crops.length === 0 ? (
        <p className="empty-state">You don&apos;t have any crops yet. Add one from &quot;My crops&quot; before running a scan.</p>
      ) : (
        <form onSubmit={submit} className="panel-block" style={{ maxWidth: 560 }}>
          <div className="form-field">
            <label>Select crop</label>
            <select
              value={form.crop_id}
              onChange={(e) => {
                const c = crops.find((x) => x.id === e.target.value)
                setForm({ ...form, crop_id: e.target.value, growth_stage: c?.growth_stage || '', district: c?.district || form.district })
              }}
              required
            >
              {crops.map((c) => <option key={c.id} value={c.id}>{c.crop} — {c.district}</option>)}
            </select>
          </div>

          {!aiCrop && (
            <div className="status-banner" style={{ background: '#eef1fb', borderLeftColor: '#5b4b8a', marginBottom: 16 }}>
              <div>
                <strong style={{ fontSize: 15 }}>Image detection coming soon for {selectedCrop?.crop}</strong>
                <p>The image model currently covers Tomato, Potato and Corn. You can still report pests and view curated advisories for this crop. Uploading a leaf image will return weather- and stage-based risk instead of a disease label.</p>
                <div style={{ display: 'flex', gap: 14, marginTop: 8 }}>
                  <Link href="/report-pest" className="inline-link">Report a pest →</Link>
                  <Link href="/treatment-guide" className="inline-link">View advisories →</Link>
                </div>
              </div>
            </div>
          )}
          <div className="form-field">
            <label>Growth stage</label>
            <select value={form.growth_stage} onChange={(e) => setForm({ ...form, growth_stage: e.target.value })} required>
              {stages.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>District</label>
            <select value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })} required>
              {meta.districts.map((d) => <option key={d}>{d}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Symptoms (optional)</label>
            <textarea rows={3} value={form.symptoms} onChange={(e) => setForm({ ...form, symptoms: e.target.value })} placeholder="What have you noticed on the leaves?" />
          </div>
          <div className="form-field">
            <label>Leaf image</label>
            <label className="upload-zone" style={{ minHeight: 120 }}>
              <input ref={fileRef} type="file" accept="image/*" capture="environment" onChange={onFile} required />
              <span className="upload-symbol"><Upload size={20} /></span>
              <strong>Upload or capture image</strong>
              <small>JPG, PNG or WebP up to 10MB</small>
            </label>
            {preview && <img src={preview} alt="Preview" style={{ marginTop: 12, maxHeight: 200, width: '100%', objectFit: 'cover' }} />}
          </div>
          {error && <p style={{ color: '#a5432a', fontSize: 12, marginBottom: 12 }}>{error}</p>}
          <button type="submit" className="button button-dark button-block" disabled={loading}>
            {loading ? 'Analyzing…' : 'Analyze crop'} <ArrowRight size={16} />
          </button>
        </form>
      )}
    </AppShell>
  )
}
