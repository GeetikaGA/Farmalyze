'use client'

import { ArrowRight, Camera } from 'lucide-react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import RiskBadge from '@/components/RiskBadge'
import api from '@/lib/api'
import { useAuth } from '@/lib/auth-context'
import type { Crop } from '@/lib/types'

export default function CropDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const lang = user?.language || 'en'
  const [crop, setCrop] = useState<Crop | null>(null)

  useEffect(() => {
    api.get(`/crops/${id}`).then((r) => setCrop(r.data))
  }, [id])

  return (
    <AppShell eyebrow="Field workspace" title={crop ? crop.crop : 'Crop detail'} roles={['farmer']}>
      {!crop ? (
        <p className="empty-state">Loading…</p>
      ) : (
        <div className="panel-block" style={{ maxWidth: 520 }}>
          <h2>{crop.crop}</h2>
          <p className="lede">{crop.variety || 'No variety noted'} · {crop.growth_stage}</p>
          <p style={{ color: 'var(--muted)', fontSize: 13, marginTop: -14, marginBottom: 20 }}>{crop.district}</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 22 }}>
            <span style={{ fontSize: 11, color: 'var(--muted)' }}>Current risk:</span>
            <RiskBadge level={crop.current_risk?.level || 'low'} lang={lang} />
            <span style={{ fontSize: 12 }}>{crop.current_risk?.score ?? 0}/100</span>
          </div>
          <Link className="button button-dark" href="/scan">
            <Camera size={16} /> Scan this crop <ArrowRight size={16} />
          </Link>
        </div>
      )}
    </AppShell>
  )
}
