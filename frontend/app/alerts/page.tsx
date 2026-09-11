'use client'

import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Alert } from '@/lib/types'

export default function AlertsPage() {
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [alerts, setAlerts] = useState<Alert[]>([])

  const load = () => api.get('/alerts').then((r) => setAlerts(r.data))

  useEffect(() => {
    load()
  }, [])

  const markRead = async (id: string) => {
    await api.patch(`/alerts/${id}/read`, { read: true })
    load()
  }

  return (
    <AppShell eyebrow="Stay ahead" title={<>Your <i>alerts.</i></>} roles={['farmer']}>
      {alerts.length === 0 ? (
        <p className="empty-state">{t(lang, 'noAlerts')}</p>
      ) : (
        <div style={{ display: 'grid', gap: 12 }}>
          {alerts.map((a) => (
            <div key={a.id} className={`alert-card severity-${a.severity} ${!a.read_status ? 'is-unread' : ''}`}>
              <div className="alert-top">
                <RiskBadge level={a.severity} lang={lang} />
                {!a.read_status && (
                  <button className="mark-read-btn" onClick={() => markRead(a.id)}>Mark read</button>
                )}
              </div>
              <p className="message">{a.message}</p>
              <p className="meta">{a.district} · {new Date(a.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </AppShell>
  )
}
