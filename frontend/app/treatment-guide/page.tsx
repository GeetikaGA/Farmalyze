'use client'

import { ChevronDown, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import AppShell from '@/components/AppShell'
import api from '@/lib/api'

interface TreatmentEntry {
  key: string
  crop: string
  disease: string
  symptoms: string
  immediate_actions: string[]
  preventive_measures: string[]
  monitoring: string[]
  escalation_conditions?: string[]
  source: string
}

function TreatmentCard({ entry, open, onToggle }: { entry: TreatmentEntry; open: boolean; onToggle: () => void }) {
  return (
    <div className="info-card">
      <button className={open ? 'accordion-toggle open' : 'accordion-toggle'} onClick={onToggle}>
        <span>
          <strong style={{ display: 'block', fontSize: 14 }}>{entry.disease}</strong>
          <span style={{ color: 'var(--muted)', fontSize: 11 }}>{entry.crop}</span>
        </span>
        <ChevronDown size={16} className="chevron" />
      </button>

      {open && (
        <div className="accordion-body">
          <p>{entry.symptoms}</p>

          <h4>Immediate actions</h4>
          <ul>{entry.immediate_actions.map((a) => <li key={a}>{a}</li>)}</ul>

          <h4>Preventive measures</h4>
          <ul>{entry.preventive_measures.map((a) => <li key={a}>{a}</li>)}</ul>

          <h4>Monitoring</h4>
          <ul>{entry.monitoring.map((a) => <li key={a}>{a}</li>)}</ul>

          {entry.escalation_conditions && entry.escalation_conditions.length > 0 && (
            <div className="escalation-box">
              <strong style={{ display: 'block', marginBottom: 4 }}>Seek expert help if:</strong>
              <ul style={{ margin: 0, paddingLeft: 16 }}>
                {entry.escalation_conditions.map((a) => <li key={a}>{a}</li>)}
              </ul>
            </div>
          )}

          <p className="source-note">Source: {entry.source}</p>
        </div>
      )}
    </div>
  )
}

export default function TreatmentGuidePage() {
  const [entries, setEntries] = useState<TreatmentEntry[]>([])
  const [query, setQuery] = useState('')
  const [cropFilter, setCropFilter] = useState('all')
  const [openKey, setOpenKey] = useState<string | null>(null)

  useEffect(() => {
    api.get('/treatments').then((r) => setEntries(r.data || []))
  }, [])

  const crops = useMemo(() => ['all', ...Array.from(new Set(entries.map((e) => e.crop)))], [entries])

  const filtered = entries.filter((e) => {
    const matchesCrop = cropFilter === 'all' || e.crop === cropFilter
    const q = query.toLowerCase()
    const matchesQuery = !q || e.disease.toLowerCase().includes(q) || e.crop.toLowerCase().includes(q)
    return matchesCrop && matchesQuery
  })

  return (
    <AppShell eyebrow="Field reference" title={<>Treatment <i>guide.</i></>}>
      <p style={{ color: 'var(--muted)', fontSize: 13, maxWidth: 560, marginBottom: 20 }}>
        Curated management guidance — not AI-generated advice. Always confirm with a local extension officer before
        applying chemicals.
      </p>

      <div className="filter-bar">
        <div className="search-wrap">
          <Search size={14} />
          <input
            placeholder="Search disease or crop..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <select value={cropFilter} onChange={(e) => setCropFilter(e.target.value)}>
          {crops.map((c) => (
            <option key={c} value={c}>{c === 'all' ? 'All crops' : c}</option>
          ))}
        </select>
      </div>

      {filtered.length === 0 ? (
        <p className="empty-state">No matching entries.</p>
      ) : (
        <div className="grid-2">
          {filtered.map((entry) => (
            <TreatmentCard
              key={entry.key}
              entry={entry}
              open={openKey === entry.key}
              onToggle={() => setOpenKey(openKey === entry.key ? null : entry.key)}
            />
          ))}
        </div>
      )}
    </AppShell>
  )
}
