'use client'

import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import api, { mediaUrl } from '@/lib/api'
import type { PendingReviewItem } from '@/lib/types'

export default function ExpertReviewsPage() {
  const [pending, setPending] = useState<PendingReviewItem[]>([])
  const [selected, setSelected] = useState<PendingReviewItem | null>(null)
  const [form, setForm] = useState({ decision: 'confirm' as 'confirm' | 'correct' | 'uncertain', final_diagnosis: '', remarks: '' })
  const [submitting, setSubmitting] = useState(false)

  const load = () => api.get('/expert/pending').then((r) => setPending(r.data))

  useEffect(() => {
    load()
  }, [])

  const select = (p: PendingReviewItem) => {
    setSelected(p)
    setForm({ decision: 'confirm', final_diagnosis: p.disease, remarks: '' })
  }

  const submitReview = async () => {
    if (!selected) return
    setSubmitting(true)
    try {
      await api.post('/expert/review', {
        prediction_id: selected.id,
        decision: form.decision,
        final_diagnosis: form.final_diagnosis || selected.disease,
        remarks: form.remarks,
      })
      setSelected(null)
      load()
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AppShell eyebrow="Verification desk" title={<>Pending <i>reviews.</i></>} roles={['expert']}>
      <div className="review-layout">
        <div className="review-list-col">
          {pending.length === 0 ? (
            <p className="empty-state">No pending requests.</p>
          ) : (
            pending.map((p) => (
              <button key={p.id} onClick={() => select(p)} className={`review-card selectable ${selected?.id === p.id ? 'active' : ''}`}>
                <strong>{p.crop} — {p.disease}</strong>
                <p style={{ color: 'var(--muted)', fontSize: 12 }}>{(p.confidence * 100).toFixed(0)}% · {p.district}</p>
              </button>
            ))
          )}
        </div>
        {selected && (
          <div className="panel-block" style={{ marginBottom: 0 }}>
            {selected.image_url && <img src={mediaUrl(selected.image_url)} alt="" className="diagnosis-image" />}
            <p style={{ fontSize: 13 }}><strong>AI:</strong> {selected.disease} ({(selected.confidence * 100).toFixed(0)}%)</p>
            <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 4 }}>
              {selected.crop} · {selected.district} · {selected.field_observation?.symptoms || 'No symptoms noted'}
            </p>
            <div style={{ marginTop: 18, display: 'grid', gap: 12 }}>
              <div className="form-field">
                <label>Decision</label>
                <select value={form.decision} onChange={(e) => setForm({ ...form, decision: e.target.value as typeof form.decision })}>
                  <option value="confirm">Confirm</option>
                  <option value="correct">Correct</option>
                  <option value="uncertain">Uncertain</option>
                </select>
              </div>
              {form.decision === 'correct' && (
                <div className="form-field">
                  <label>Correct diagnosis</label>
                  <input value={form.final_diagnosis} onChange={(e) => setForm({ ...form, final_diagnosis: e.target.value })} />
                </div>
              )}
              <div className="form-field">
                <label>Remarks</label>
                <textarea rows={3} value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} />
              </div>
              <button onClick={submitReview} className="button button-dark button-block" disabled={submitting}>
                {submitting ? 'Submitting…' : 'Submit review'}
              </button>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  )
}
