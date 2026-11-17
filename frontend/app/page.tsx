
"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const IndonesiaMap = dynamic(
  () => import("@/src/components/IndonesiaMap"),
  { ssr: false }
);

interface ApiStatus {
  success: boolean;
  system: string;
  region: string;
  satellite: string;
  method: string;
  status: string;
}

const statistics = [
  {
    label: "Total Provinsi",
    value: "38",
    detail: "Seluruh wilayah Indonesia",
    icon: "◈",
  },
  {
    label: "Kabupaten",
    value: "422",
    detail: "Wilayah administrasi",
    icon: "⌂",
  },
  {
    label: "Kota",
    value: "98",
    detail: "Wilayah administrasi",
    icon: "▦",
  },
  {
    label: "Satellite Data",
    value: "Sentinel-2",
    detail: "Earth observation imagery",
    icon: "◎",
  },
];

const navigation = [
  { label: "Overview", icon: "▦", href: "#dashboard" },
  { label: "Monitoring Map", icon: "◎", href: "#monitoring" },
  { label: "Area Selection", icon: "⌖", href: "#area-selection" },
  { label: "Satellite Imagery", icon: "◉", href: "#satellite" },
  { label: "Fire Analysis", icon: "◈", href: "#analysis" },
];

export default function Home() {
  const [data, setData] = useState<ApiStatus | null>(null);
  const [error, setError] = useState("");
  const [activeNav, setActiveNav] = useState("Overview");

  useEffect(() => {
    const controller = new AbortController();

    fetch("http://127.0.0.1:8000/api/status", {
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) throw new Error("API Error");
        return response.json();
      })
      .then((result: ApiStatus) => {
        setData(result);
        setError("");
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          setError("Backend tidak terhubung");
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <main className="rimbara-layout" id="dashboard">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">R</div>
          <div>
            <h1>RIMBARA</h1>
            <span>FOREST INTELLIGENCE</span>
          </div>
        </div>

        <div className="sidebar-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map((item) => (
            <a
              key={item.label}
              href={item.href}
              onClick={() => setActiveNav(item.label)}
              className={`nav-item ${
                activeNav === item.label ? "active" : ""
              }`}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {activeNav === item.label && (
                <span className="active-indicator" />
              )}
            </a>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-info">
            <div className="info-icon">✳</div>
            <div>
              <strong>RIMBARA SYSTEM</strong>
              <p>Forest monitoring platform</p>
            </div>
          </div>

          <div className="sidebar-version">
            <span>VERSION 1.0.0</span>
            <span>© 2026 RIMBARA</span>
          </div>
        </div>

      </aside>

      {/* MAIN CONTENT */}
      <section className="main-content">

        {/* TOPBAR */}
        <header className="topbar">
          <div>
            <div className="breadcrumb">
              Workspace <span>/</span> Overview
            </div>
            <p className="topbar-subtitle">
              Forest monitoring and geospatial intelligence
            </p>
          </div>

          <div className="topbar-right">
            <div className={`system-status ${data ? "online" : "offline"}`}>
              <span className="status-dot" />
              {data ? "SYSTEM ONLINE" : error || "CONNECTING"}
            </div>

            <div className="profile-avatar">R</div>
          </div>
        </header>

        {/* PAGE HEADER */}
        <div className="page-heading">
          <div>
            <div className="eyebrow">
              <span className="eyebrow-line" />
              NATIONAL MONITORING SYSTEM
            </div>

            <h2>
              Forest <span>Overview.</span>
            </h2>

            <p>
              Pusat pemantauan dan analisis kebakaran hutan
              berbasis penginderaan jauh untuk wilayah Indonesia.
            </p>
          </div>

          <div className="date-label">
            <span>◷</span>
            NATIONAL COVERAGE
          </div>
        </div>

        {/* STATISTICS */}
        <section className="stats-grid">

          {statistics.map((item, index) => (
            <div className="stat-card" key={item.label}>
              <div className="stat-top">
                <span className="stat-label">{item.label}</span>
                <span className="stat-icon">{item.icon}</span>
              </div>

              <h3 className={index === 3 ? "satellite-value" : ""}>
                {item.value}
              </h3>

              <p>{item.detail}</p>

              <div className="stat-decoration" />
            </div>
          ))}

        </section>

        {/* MAP SECTION */}
        <section className="content-grid" id="monitoring">

          <div className="map-card">

            <div className="section-heading">
              <div>
                <div className="section-eyebrow">
                  GEOSPATIAL MONITORING
                </div>
                <h3>Indonesia Monitoring Map</h3>
                <p>
                  Peta interaktif untuk pemantauan wilayah nasional.
                </p>
              </div>

              <span className="map-badge">
                <span className="status-dot" />
                INTERACTIVE MAP
              </span>
            </div>

            <div className="map-wrapper">
              <IndonesiaMap />
            </div>

            <div className="map-footer">
              <div className="map-legend">
                <span className="legend-dot" />
                Base map
              </div>

              <span className="map-coordinates">
                INDONESIA · 6°N – 11°S
              </span>
            </div>

          </div>

          {/* RIGHT PANEL */}
          <aside className="right-panel">

            <div className="panel-card" id="area-selection">
              <div className="panel-heading">
                <div className="panel-icon">⌖</div>
                <span>AREA COVERAGE</span>
              </div>

              <h3>National Scale</h3>

              <p>
                Cakupan pemantauan mencakup seluruh provinsi
                dan wilayah kabupaten/kota di Indonesia.
              </p>

              <div className="coverage-item">
                <span>Provinsi</span>
                <strong>38</strong>
              </div>

              <div className="coverage-item">
                <span>Kabupaten</span>
                <strong>422</strong>
              </div>

              <div className="coverage-item">
                <span>Kota</span>
                <strong>98</strong>
              </div>
            </div>

            <div className="panel-card satellite-card" id="satellite">
              <div className="panel-heading">
                <div className="panel-icon">◎</div>
                <span>SATELLITE SOURCE</span>
              </div>

              <h3>Sentinel-2</h3>

              <p>
                Multispectral satellite imagery for
                vegetation and burned area monitoring.
              </p>

              <div className="satellite-tag">
                COPERNICUS DATA SPACE
              </div>
            </div>

            <div className="panel-card analysis-card" id="analysis">
              <div className="panel-heading">
                <div className="panel-icon">◈</div>
                <span>ANALYSIS METHOD</span>
              </div>

              <h3>dNBR Analysis</h3>

              <p>
                Differenced Normalized Burn Ratio untuk
                analisis perubahan kondisi vegetasi
                akibat kebakaran.
              </p>

              <div className="analysis-formula">
                dNBR = NBRpre - NBRpost
              </div>
            </div>

          </aside>

        </section>

        {/* BOTTOM INFORMATION */}
        <section className="bottom-banner">
          <div className="banner-icon">✳</div>

          <div>
            <strong>RIMBARA Forest Intelligence</strong>
            <p>
              Satellite-based forest fire monitoring and
              geospatial analysis platform.
            </p>
          </div>

          <div className="banner-right">
            <span className="status-dot" />
            {data ? "Connected to API" : "API unavailable"}
          </div>
        </section>

        <footer className="footer">
          <span>© 2026 RIMBARA · Forest Intelligence Platform</span>
          <span>Powered by Sentinel-2 & dNBR</span>
        </footer>

      </section>
    </main>
  );
}
