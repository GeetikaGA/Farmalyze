'use client'

import AppShell from '@/components/AppShell'

const FAQS = [
  {
    q: 'How accurate is the disease detection?',
    a: 'The AI model gives a confidence score with every result. Low or medium confidence results are automatically flagged for expert review — always treat AI results as a first opinion, not a final diagnosis.',
  },
  {
    q: 'What should I do with a high-risk alert?',
    a: 'Open the alert to see the recommended immediate actions and, if suggested, request expert verification before applying any chemical treatment.',
  },
  {
    q: 'Why was my image rejected?',
    a: 'Images that are too blurry, too dark, or too low-resolution are rejected before analysis so the AI doesn\u2019t guess from a poor photo. Retake the photo in good light, focused on the affected area.',
  },
  {
    q: 'Who reviews my verification requests?',
    a: 'Verified agricultural experts registered on the platform. They see your image, symptoms, and the AI\u2019s prediction, and confirm, correct, or mark it uncertain.',
  },
]

export default function HelpPage() {
  return (
    <AppShell eyebrow="We're here to help" title={<>Help & <i>support.</i></>}>
      <div className="help-layout">
        <div style={{ display: 'grid', gap: 12 }}>
          {FAQS.map((f) => (
            <div key={f.q} className="info-card faq-card">
              <strong style={{ fontSize: 14 }}>{f.q}</strong>
              <p className="answer">{f.a}</p>
            </div>
          ))}
        </div>

        <div className="info-card">
          <h2 style={{ fontFamily: 'Georgia, serif', fontWeight: 400, fontSize: 20, margin: '0 0 4px' }}>Still need help?</h2>
          <p style={{ color: 'var(--muted)', fontSize: 13, margin: '0 0 14px' }}>
            Reach the platform team, or contact your local agriculture extension office for urgent field issues.
          </p>
          <div>
            <div className="contact-row"><span className="label">Support</span><span>support@farmalyze.example</span></div>
            <div className="contact-row"><span className="label">Extension helpline</span><span>1800-XXX-XXXX</span></div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
