'use client'

import { Users } from 'lucide-react'
import AppShell from '@/components/AppShell'

export default function CommunityPage() {
  return (
    <AppShell eyebrow="Coming soon" title={<>Community.</>}>
      <div className="info-card coming-soon-block">
        <Users size={32} />
        <strong>Farmer community is on the way</strong>
        <p>
          Soon you&apos;ll be able to swap field notes, ask fellow farmers about local outbreaks, and see what&apos;s
          working in your district. Check back shortly.
        </p>
      </div>
    </AppShell>
  )
}
