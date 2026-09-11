'use client'

import { useEffect, useRef } from 'react'
import type { DistrictRisk, RiskLevel } from '@/lib/types'

const LEAFLET_CSS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'

const LEVEL_COLOR: Record<RiskLevel, string> = {
  high: '#a5432a',
  moderate: '#d9a441',
  low: '#6b8f4e',
}
const NO_DATA_COLOR = '#d8ddd0'

function ensureLeafletCss() {
  if (typeof document === 'undefined') return
  if (document.querySelector(`link[href="${LEAFLET_CSS}"]`)) return
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = LEAFLET_CSS
  document.head.appendChild(link)
}

export default function MaharashtraRiskMap({
  districts,
  onSelect,
}: {
  districts: DistrictRisk[]
  onSelect?: (d: DistrictRisk) => void
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<any>(null)
  const layerRef = useRef<any>(null)
  const dataRef = useRef<Record<string, DistrictRisk>>({})

  // Keep a name->risk lookup fresh without re-initialising the map.
  useEffect(() => {
    const map: Record<string, DistrictRisk> = {}
    for (const d of districts) map[d.district.toLowerCase()] = d
    dataRef.current = map
    if (layerRef.current) layerRef.current.setStyle(styleFor)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [districts])

  function riskFor(name?: string): DistrictRisk | undefined {
    if (!name) return undefined
    return dataRef.current[name.toLowerCase()]
  }

  function styleFor(feature: any) {
    const risk = riskFor(feature?.properties?.district)
    const color = risk ? LEVEL_COLOR[risk.risk_level] : NO_DATA_COLOR
    return {
      fillColor: color,
      fillOpacity: risk ? 0.72 : 0.35,
      color: '#ffffff',
      weight: 1,
    }
  }

  useEffect(() => {
    let cancelled = false
    ensureLeafletCss()

    ;(async () => {
      const L = (await import('leaflet')).default ?? (await import('leaflet'))
      if (cancelled || !containerRef.current || mapRef.current) return

      const map = L.map(containerRef.current, {
        center: [19.2, 76.5],
        zoom: 6,
        scrollWheelZoom: false,
        attributionControl: true,
      })
      mapRef.current = map

      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        maxZoom: 19,
      }).addTo(map)

      let geo: any
      try {
        const res = await fetch('/maharashtra-districts.geojson')
        geo = await res.json()
      } catch {
        return
      }
      if (cancelled) return

      const popupHtml = (d?: DistrictRisk, name?: string) => {
        if (!d) return `<div class="mh-popup"><strong>${name ?? ''}</strong><p class="mh-nodata">No active reports.</p></div>`
        const threats = d.threats
          .slice(0, 4)
          .map(
            (t) =>
              `<li><span class="mh-dot mh-${t.risk_level}"></span>${t.name} <em>(${t.kind})</em> — ${t.risk_score}</li>`,
          )
          .join('')
        const crops = d.crops_affected.length ? d.crops_affected.join(', ') : '—'
        const forecast =
          typeof d.outbreak_forecast === 'number'
            ? `<p class="mh-row"><b>Predicted outbreak:</b> ${d.outbreak_forecast}%</p>`
            : ''
        return `<div class="mh-popup">
          <strong>${d.district}</strong>
          <span class="mh-badge mh-${d.risk_level}">${d.risk_level.toUpperCase()} · ${d.risk_score}/100</span>
          <ul class="mh-threats">${threats}</ul>
          <p class="mh-row"><b>Crops:</b> ${crops}</p>
          ${forecast}
          <p class="mh-action">${d.recommended_action}</p>
        </div>`
      }

      const layer = L.geoJSON(geo, {
        style: styleFor,
        onEachFeature: (feature: any, lyr: any) => {
          const name = feature?.properties?.district
          lyr.on({
            mouseover: () => lyr.setStyle({ weight: 2.5, color: '#1e2a23' }),
            mouseout: () => layer.resetStyle(lyr),
            click: () => {
              const d = riskFor(name)
              lyr.bindPopup(popupHtml(d, name), { maxWidth: 280 }).openPopup()
              if (d && onSelect) onSelect(d)
            },
          })
        },
      }).addTo(map)
      layerRef.current = layer

      try {
        map.fitBounds(layer.getBounds(), { padding: [10, 10] })
      } catch {
        /* ignore */
      }
    })()

    return () => {
      cancelled = true
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
        layerRef.current = null
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return <div ref={containerRef} className="mh-map" />
}
