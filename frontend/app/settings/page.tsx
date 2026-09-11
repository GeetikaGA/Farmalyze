'use client'

import AppShell from '@/components/AppShell'
import { useAuth } from '@/lib/auth-context'
import type { Language } from '@/lib/types'

export default function SettingsPage() {
  const { user, setLanguage } = useAuth()
  const lang = user?.language || 'en'

  return (
    <AppShell eyebrow="Your account" title={<>Settings.</>}>
      <div className="panel-block" style={{ maxWidth: 460 }}>
        <h2 style={{ fontSize: 20, marginBottom: 4 }}>Account</h2>
        <div className="account-row"><span className="label">Name</span><span>{user?.name}</span></div>
        <div className="account-row"><span className="label">Email</span><span>{user?.email}</span></div>
        <div className="account-row"><span className="label">Role</span><span style={{ textTransform: 'capitalize' }}>{user?.role}</span></div>
      </div>

      <div className="panel-block" style={{ maxWidth: 460 }}>
        <h2 style={{ fontSize: 20, marginBottom: 12 }}>Language</h2>
        <div className="form-field" style={{ marginBottom: 0 }}>
          <label>Preferred language</label>
          <select value={lang} onChange={(e) => setLanguage(e.target.value as Language)}>
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="mr">मराठी</option>
          </select>
        </div>
      </div>
    </AppShell>
  )
}
