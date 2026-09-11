'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import type { ExpertDashboardData } from '@/lib/types'

export default function ExpertDashboardPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [data, setData] = useState<ExpertDashboardData | null>(null)

  useEffect(() => {
    api.get('/expert/dashboard').then((r) => setData(r.data))
  }, [])

  return (
    <AppShell eyebrow="Verification desk" title={<>Expert <i>dashboard.</i></>} roles={['expert']}>
      {!data ? (
        <p className="empty-state">Loading…</p>
      ) : (
        <>
          <div className="grid-3" style={{ marginBottom: 24 }}>
            <div className="stat-card"><strong>{data.pending_verifications}</strong><span>Pending</span></div>
            <div className="stat-card"><strong>{data.confirmed_cases}</strong><span>Confirmed</span></div>
            <div className="stat-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Link className="button button-dark button-block" href="/expert/reviews">Review queue</Link>
            </div>
          </div>
          <div className="panel-block">
            <h2>District hotspots</h2>
            <div className="grid-2">
              {data.hotspots?.map((h) => (
                <div key={`${h.district}-${h.disease}`} className="hotspot-card" style={{ padding: '14px 16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div><strong>{h.district}</strong><p className="disease" style={{ margin: '2px 0 0' }}>{h.disease}</p></div>
                    <RiskBadge level={h.risk_level} lang={lang} />
                  </div>
                </div>
              ))}
            </div>
          </div>
          {data.recent_reviews?.length > 0 && (
            <div className="panel-block">
              <h2>Recent reviews</h2>
              <div style={{ overflowX: 'auto' }}>
                <table className="data-table">
                  <thead><tr><th>Diagnosis</th><th>Decision</th><th>Expert</th><th>When</th></tr></thead>
                  <tbody>
                    {data.recent_reviews.map((r) => (
                      <tr key={r.id}>
                        <td>{r.final_diagnosis}</td>
                        <td style={{ textTransform: 'capitalize' }}>{r.decision}</td>
                        <td>{r.expert_name}</td>
                        <td>{new Date(r.reviewed_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          <p style={{ fontSize: 11, color: 'var(--muted)' }}>{data.note}</p>
        </>
      )}
    </AppShell>
  )
}
