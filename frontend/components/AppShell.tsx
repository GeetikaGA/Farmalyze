'use client'

import {
  Activity,
  Bell,
  BookOpen,
  Bug,
  Camera,
  CircleHelp,
  ClipboardCheck,
  History as HistoryIcon,
  Landmark,
  LogOut,
  Menu,
  Settings as SettingsIcon,
  Sprout,
  TrendingUp,
  Users,
  X,
} from 'lucide-react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useEffect, useState, type ReactNode } from 'react'
import { useAuth } from '@/lib/auth-context'
import { t } from '@/lib/i18n'
import type { Role } from '@/lib/types'

const logo = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-qqhPMzkQclfyzhmOo9RxoxBi3HetjO.png'

const farmerNav = [
  { href: '/dashboard', key: 'dashboard', icon: Activity },
  { href: '/scan', key: 'scanCrop', icon: Camera },
  { href: '/report-pest', key: 'navReportPest', icon: Bug },
  { href: '/crops', key: 'myCrops', icon: Sprout },
  { href: '/alerts', key: 'alerts', icon: Bell },
  { href: '/risk-map', key: 'riskMap', icon: TrendingUp },
  { href: '/history', key: 'history', icon: HistoryIcon },
  { href: '/treatment-guide', key: 'navTreatmentGuide', icon: BookOpen },
  { href: '/community', key: 'navCommunity', icon: Users },
] as const

const expertNav = [
  { href: '/expert', key: 'expertDashboard', icon: Activity },
  { href: '/expert/reviews', key: 'pendingReviews', icon: ClipboardCheck },
  { href: '/risk-map', key: 'riskMap', icon: TrendingUp },
  { href: '/treatment-guide', key: 'navTreatmentGuide', icon: BookOpen },
] as const

const officialNav = [
  { href: '/official', key: 'navOfficialDashboard', icon: Landmark },
  { href: '/risk-map', key: 'riskMap', icon: TrendingUp },
  { href: '/treatment-guide', key: 'navTreatmentGuide', icon: BookOpen },
] as const

function initials(name?: string) {
  if (!name) return '··'
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase())
    .join('')
}

export default function AppShell({
  children,
  eyebrow,
  title,
  roles,
  headerExtra,
}: {
  children: ReactNode
  eyebrow: string
  title: ReactNode
  roles?: Role[]
  headerExtra?: ReactNode
}) {
  const { user, logout, initializing } = useAuth()
  const router = useRouter()
  const pathname = usePathname()
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (initializing) return
    if (!user) {
      router.replace('/login')
      return
    }
    if (roles && !roles.includes(user.role)) {
      const home = user.role === 'expert' ? '/expert' : user.role === 'official' ? '/official' : '/dashboard'
      router.replace(home)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initializing, user])

  if (initializing || !user || (roles && !roles.includes(user.role))) {
    return (
      <main className="dashboard-shell">
        <div style={{ padding: 60, color: 'var(--muted)', fontSize: 13 }}>Loading…</div>
      </main>
    )
  }

  const isExpert = user.role === 'expert'
  const isOfficial = user.role === 'official'
  const nav = isOfficial ? officialNav : isExpert ? expertNav : farmerNav
  const lang = user.language
  const workspaceKicker = isOfficial ? 'surveillanceDesk' : isExpert ? 'verificationDesk' : 'fieldWorkspace'
  const workspaceName = isOfficial ? 'officialConsole' : isExpert ? 'agriOfficerConsole' : null

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  return (
    <main className="dashboard-shell">
      <aside className={open ? 'dashboard-sidebar open' : 'dashboard-sidebar'}>
        <Link href="/" className="dashboard-logo">
          <img src={logo} alt="Farmalyze" />
        </Link>
        <div className="workspace">
          <span>{t(lang, workspaceKicker)}</span>
          <strong>{workspaceName ? t(lang, workspaceName) : user.name}</strong>
          <small>{t(lang, 'connectedStatus')}</small>
        </div>
        <nav className="dash-nav">
          {nav.map(({ href, key, icon: Icon }) => (
            <Link key={href} href={href} className={pathname === href ? 'active' : ''} onClick={() => setOpen(false)}>
              <Icon size={17} />
              {t(lang, key)}
            </Link>
          ))}
        </nav>
        <div className="dash-bottom">
          <Link href="/settings" onClick={() => setOpen(false)} className={pathname === '/settings' ? 'active' : ''}>
            <SettingsIcon size={17} /> {t(lang, 'settings')}
          </Link>
          <Link href="/help" onClick={() => setOpen(false)} className={pathname === '/help' ? 'active' : ''}>
            <CircleHelp size={17} /> {t(lang, 'supportCentre')}
          </Link>
          <a href="#logout" onClick={(e) => { e.preventDefault(); handleLogout() }}>
            <LogOut size={17} /> {t(lang, 'logout')}
          </a>
        </div>
      </aside>
      <section className="dashboard-main">
        <header className="dashboard-header">
          <button className="dash-menu" onClick={() => setOpen(!open)} aria-label="Toggle menu">
            {open ? <X /> : <Menu />}
          </button>
          <div>
            <p className="section-kicker">{eyebrow}</p>
            <h1>{title}</h1>
          </div>
          <div className="header-actions">
            {headerExtra}
            <div className="avatar">{initials(user.name)}</div>
          </div>
        </header>
        <div className="dash-content">{children}</div>
      </section>
    </main>
  )
}
