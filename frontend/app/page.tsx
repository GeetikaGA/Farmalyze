'use client'

import { useState } from 'react'
import { ArrowRight, Check, ChevronDown, Leaf, Menu, ShieldCheck, Sparkles, Upload, X } from 'lucide-react'

const images = {
  logo: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-qqhPMzkQclfyzhmOo9RxoxBi3HetjO.png',
  field: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-IpnCmA0I8GQmifXnQnXANH5RM3TaLr.png',
  farmers: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-3ek6ipJg7H7NiUzVvKWkNdqfQHzixm.png',
  harvest: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-QXMCNna5teLGPf6MRFl3i0e1iiPm2L.png',
  greens: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-swmZb8GGSnvwGTMaTo9eRHgv5APwI2.png',
}

export default function Page() {
  const [loginOpen, setLoginOpen] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <main className="site-shell">
      <nav className="nav-wrap" aria-label="Main navigation">
        <a className="brand" href="#top" aria-label="Farmalyze home">
          <img className="brand-logo" src={images.logo} alt="Farmalyze" />
        </a>
        <div className={`nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a href="#how-it-works" onClick={() => setMenuOpen(false)}>How it works</a>
          <a href="#impact" onClick={() => setMenuOpen(false)}>Our impact</a>
          <a href="#about" onClick={() => setMenuOpen(false)}>About us</a>
          <button className="nav-login" onClick={() => { window.location.href = '/login' }}>Log in <ArrowRight size={15} /></button>
        </div>
        <button className="menu-toggle" aria-label="Toggle navigation" onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? <X /> : <Menu />}</button>
      </nav>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow"><span className="eyebrow-line" /> Technology for healthier harvests</p>
          <h1>When crops<br /><span>thrive,</span> communities<br />grow.</h1>
          <p className="hero-text">Early answers for the people who feed us. Detect crop diseases from a single leaf image, before a small problem becomes a lost harvest.</p>
          <div className="hero-actions">
            <button className="button button-dark" onClick={() => { window.location.href = '/login' }}>Start a diagnosis <ArrowRight size={17} /></button>
            <a className="text-link" href="#how-it-works">See how it works <span>↓</span></a>
          </div>
          <div className="trust-note"><ShieldCheck size={17} /> Built for farmers, agronomists & field teams</div>
          <p className="mandate-line">A field-ready decision support system for resilient agriculture.</p>
        </div>
        <div className="hero-visual">
          <div className="hero-image-wrap"><img src={images.field} alt="A hand inspecting wheat in a field" /></div>
          <div className="hero-stamp"><Sparkles size={15} /><span>Powered by<br /><strong>care + science</strong></span></div>
          <div className="hero-caption">01 <span /> Healthy crops, stronger futures</div>
        </div>
      </section>

      <section className="intro-band" id="how-it-works">
        <p className="section-kicker">A clearer way forward</p>
        <div className="intro-grid">
          <h2>Small signs.<br /><i>Big difference.</i></h2>
          <p>Our technology turns a photo into a practical next step. No lab. No guesswork. Just clear guidance when it matters most.</p>
        </div>
        <div className="steps-row">
          <div className="step"><span>01</span><div><Upload size={21} /><h3>Capture</h3><p>Take a clear photo of the affected leaf.</p></div></div>
          <div className="step"><span>02</span><div><Sparkles size={21} /><h3>Understand</h3><p>Our model identifies signs of disease.</p></div></div>
          <div className="step"><span>03</span><div><Check size={21} /><h3>Act early</h3><p>Get a simple, informed recommendation.</p></div></div>
        </div>
      </section>

      <section className="story-section" id="impact">
        <div className="story-image"><img src={images.farmers} alt="Farmers planting rice seedlings in a field" /></div>
        <div className="story-copy"><p className="section-kicker">Technology with a human centre</p><h2>Built around the<br /><i>field,</i> not the lab.</h2><p>For a farmer, a crop is more than a number. It is a season of work, a family&apos;s security, and food on a table. We make advanced crop intelligence feel simple, useful, and close at hand.</p><a className="arrow-link" href="#about">Meet the people behind it <ArrowRight size={17} /></a></div>
      </section>

      <section className="visual-strip" id="about">
        <div className="strip-heading"><p className="section-kicker">From soil to screen</p><h2>Better decisions<br /><i>start early.</i></h2></div>
        <img src={images.harvest} alt="Farmers harvesting eggplant in a green field" /><img src={images.greens} alt="Rows of colorful lettuce growing in a garden" />
      </section>

      <footer className="footer"><a className="brand" href="#top" aria-label="Farmalyze home"><img className="brand-logo" src={images.logo} alt="Farmalyze" /></a><p>For healthier crops and the people who grow them.</p><button className="button button-light" onClick={() => { window.location.href = '/login' }}>Enter the platform <ArrowRight size={16} /></button></footer>

      {loginOpen && <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target) setLoginOpen(false) }}><div className="login-modal" role="dialog" aria-modal="true" aria-labelledby="login-title"><button className="modal-close" onClick={() => setLoginOpen(false)} aria-label="Close login"><X size={20} /></button><div className="login-icon"><Leaf size={22} /></div><p className="section-kicker">Welcome back</p><h2 id="login-title">Good to see you<br /><i>again.</i></h2><p className="modal-copy">Log in to access your crop health dashboard and previous diagnoses.</p><form onSubmit={(event) => event.preventDefault()}><label>Email address<input type="email" placeholder="you@example.com" required /></label><label>Password<input type="password" placeholder="••••••••" required /></label><button className="button button-dark full-width" type="submit">Log in <ArrowRight size={17} /></button></form><p className="modal-foot">New here? <button onClick={() => setLoginOpen(false)}>Start a diagnosis</button></p></div></div>}
    </main>
  )
}
