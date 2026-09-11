'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Leaf, ShieldCheck } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { useAuth } from '@/lib/auth-context'
import type { Language, Role } from '@/lib/types'

const logo = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-qqhPMzkQclfyzhmOo9RxoxBi3HetjO.png'
const farmers = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-3ek6ipJg7H7NiUzVvKWkNdqfQHzixm.png'

export default function RegisterPage() {
  const { register, loading } = useAuth()
  const router = useRouter()
  const [form, setForm] = useState<{ name: string; email: string; password: string; role: Role; language: Language }>({
    name: '',
    email: '',
    password: '',
    role: 'farmer',
    language: 'en',
  })
  const [error, setError] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const user = await register(form)
      router.push(user.role === 'expert' ? '/expert' : user.role === 'official' ? '/official' : '/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
    }
  }

  return (
    <main className="auth-shell">
      <div className="auth-visual" style={{ backgroundImage: `linear-gradient(120deg, #15241dcc, #15241d33), url(${farmers})` }}>
        <Link href="/" className="auth-logo">
          <img src={logo} alt="Farmalyze" />
        </Link>
        <div className="auth-visual-copy">
          <p className="eyebrow light"><span className="eyebrow-line" /> Join the pilot</p>
          <h1>Built for the<br /><i>field, first.</i></h1>
          <p>Farmers and agri-officers on one platform — from a single leaf photo to a trusted, verified diagnosis.</p>
        </div>
        <p className="auth-legal">Farmalyze / Government innovation program</p>
      </div>
      <div className="auth-form-wrap">
        <Link href="/" className="back-link">← Back to Farmalyze</Link>
        <motion.div className="auth-form" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <div className="auth-icon"><Leaf size={20} /></div>
          <p className="section-kicker">Get started</p>
          <h2>Create your<br /><i>account.</i></h2>
          <p className="auth-description">Set up your workspace to start scanning crops, tracking risk, and reaching a verified diagnosis faster.</p>
          <form onSubmit={submit}>
            <label>Full name
              <input type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Your name" required minLength={2} />
            </label>
            <label>Email address
              <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="you@example.com" required />
            </label>
            <label>Password
              <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="At least 6 characters" required minLength={6} />
            </label>
            <label>I am a…
              <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value as Role })}>
                <option value="farmer">Farmer</option>
                <option value="expert">Expert / agri officer</option>
                <option value="official">Government official</option>
              </select>
            </label>
            <label>Preferred language
              <select value={form.language} onChange={(e) => setForm({ ...form, language: e.target.value as Language })}>
                <option value="en">English</option>
                <option value="hi">हिंदी</option>
                <option value="mr">मराठी</option>
              </select>
            </label>
            {error && <p style={{ color: '#a5432a', fontSize: 12 }}>{error}</p>}
            <button className="button button-dark full-width" type="submit" disabled={loading}>
              {loading ? 'Creating account…' : 'Create account'} <ArrowRight size={17} />
            </button>
          </form>
          <p className="modal-foot" style={{ marginTop: 16 }}>
            Already have an account? <Link href="/login" style={{ textDecoration: 'underline', fontWeight: 700 }}>Log in</Link>
          </p>
          <div className="secure-note"><ShieldCheck size={16} /> Your data is handled securely and privately.</div>
        </motion.div>
      </div>
    </main>
  )
}
