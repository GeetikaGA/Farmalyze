'use client'

import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import AppShell from '@/components/AppShell'
import api from '@/lib/api'

interface VerifyStatus {
  prediction_id: string
  status: string
  review?: {
    expert_name: string
    final_diagnosis: string
    remarks?: string
  } | null
}

export default function VerificationPage() {
  const { id } = useParams<{ id: string }>()
  const [status, setStatus] = useState<VerifyStatus | null>(null)

  useEffect(() => {
    api.get(`/verify-status/${id}`).then((r) => setStatus(r.data))
  }, [id])

  return (
    <AppShell eyebrow="Human-in-the-loop" title={<>Verification <i>status.</i></>}>
      {!status ? (
        <p className="empty-state">Loading…</p>
      ) : (
        <div className="panel-block" style={{ maxWidth: 480 }}>
          <p style={{ textTransform: 'capitalize', fontWeight: 700, fontSize: 15 }}>Status: {status.status}</p>
          {status.review && (
            <div style={{ marginTop: 16, fontSize: 13, display: 'grid', gap: 6 }}>
              <p><strong>Expert:</strong> {status.review.expert_name}</p>
              <p><strong>Diagnosis:</strong> {status.review.final_diagnosis}</p>
              {status.review.remarks && <p><strong>Remarks:</strong> {status.review.remarks}</p>}
            </div>
          )}
          <Link href={`/prediction/${id}`} className="button button-outline" style={{ marginTop: 20 }}>
            View full diagnosis
          </Link>
        </div>
      )}
    </AppShell>
  )
}
