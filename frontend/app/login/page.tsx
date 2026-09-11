'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Leaf, ShieldCheck } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { useAuth } from '@/lib/auth-context'

const logo = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-qqhPMzkQclfyzhmOo9RxoxBi3HetjO.png'
const field = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-IpnCmA0I8GQmifXnQnXANH5RM3TaLr.png'

export default function LoginPage() {
  const { login, loading } = useAuth()
  const router = useRouter()
  const [email, setEmail] = useState('farmer@demo.com')
  const [password, setPassword] = useState('farmer123')
  const [error, setError] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const user = await login(email, password)
      router.push(user.role === 'expert' ? '/expert' : user.role === 'official' ? '/official' : '/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    }
  }

  return (
    <main className="auth-shell">
      <div className="auth-visual" style={{ backgroundImage: `linear-gradient(120deg, #15241dcc, #15241d33), url(${field})` }}>
        <Link href="/" className="auth-logo">
          <img src={logo} alt="Farmalyze" />
        </Link>
        <div className="auth-visual-copy">
          <p className="eyebrow light"><span className="eyebrow-line" /> Secure field intelligence</p>
          <h1>Clear answers<br /><i>when it matters.</i></h1>
          <p>One platform for earlier detection, better decisions, and stronger harvests.</p>
        </div>
        <p className="auth-legal">Farmalyze / Government innovation program</p>
      </div>
      <div className="auth-form-wrap">
        <Link href="/" className="back-link">← Back to Farmalyze</Link>
        <motion.div className="auth-form" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <div className="auth-icon"><Leaf size={20} /></div>
          <p className="section-kicker">Platform access</p>
          <h2>Welcome<br /><i>back.</i></h2>
          <p className="auth-description">Sign in to review crop health, run a new scan, and keep your field history in one place.</p>
          <form onSubmit={submit}>
            <label>Email address<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required /></label>
            <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" required /></label>
            <div className="form-row">
              <label className="check-row"><input type="checkbox" /> Remember me</label>
              <a href="#forgot">Forgot password?</a>
            </div>
            {error && <p style={{ color: '#a5432a', fontSize: 12 }}>{error}</p>}
            <button className="button button-dark full-width" type="submit" disabled={loading}>
              {loading ? 'Signing in…' : 'Log in'} <ArrowRight size={17} />
            </button>
          </form>
          <p className="modal-foot" style={{ marginTop: 16 }}>
            New here? <Link href="/register" style={{ textDecoration: 'underline', fontWeight: 700 }}>Create an account</Link>
          </p>
          <div className="secure-note"><ShieldCheck size={16} /> Your data is handled securely and privately.</div>
          <p style={{ marginTop: 18, fontSize: 11, color: 'var(--muted)', background: 'var(--cream)', padding: '10px 12px' }}>
            Demo: farmer@demo.com / farmer123 · expert@demo.com / expert123
          </p>
        </motion.div>
      </div>
    </main>
  )
}
