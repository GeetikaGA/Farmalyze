'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import type { Prediction } from '@/lib/types'

export default function HistoryPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [scans, setScans] = useState<Prediction[]>([])

  useEffect(() => {
    api.get('/reports').then((r) => setScans(r.data.scans || []))
  }, [])

  return (
    <AppShell eyebrow="Full record" title={<>Scan <i>history.</i></>} roles={['farmer']}>
      {scans.length === 0 ? (
        <p className="empty-state">No scans yet — run your first diagnosis from the dashboard.</p>
      ) : (
        <div className="panel-block" style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr><th>Date</th><th>Crop</th><th>Disease</th><th>Conf.</th><th>Risk</th><th>Verify</th></tr>
            </thead>
            <tbody>
              {scans.map((s) => (
                <tr key={s.id}>
                  <td>{new Date(s.timestamp).toLocaleDateString()}</td>
                  <td>{s.crop}</td>
                  <td><Link href={`/prediction/${s.id}`}>{s.disease}</Link></td>
                  <td>{(s.confidence * 100).toFixed(0)}%</td>
                  <td><RiskBadge level={s.risk?.level || 'low'} lang={lang} /></td>
                  <td style={{ textTransform: 'capitalize' }}>{s.verification_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </AppShell>
  )
}
