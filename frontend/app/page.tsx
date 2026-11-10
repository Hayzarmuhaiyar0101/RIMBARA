
"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const IndonesiaMap = dynamic(
  () =>
    import("@/src/components/IndonesiaMap").then(
      (mod) => mod.default
    ),
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

export default function Home() {
  const [data, setData] = useState<ApiStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/status")
      .then((response) => {
        if (!response.ok) throw new Error("API Error");
        return response.json();
      })
      .then(setData)
      .catch(() => setError("Backend tidak terhubung"));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white p-6 md:p-10">
      <div className="max-w-7xl mx-auto">

        <header className="flex justify-between items-center mb-10">
          <div>
            <p className="text-emerald-400 text-sm tracking-widest">
              NATIONAL FOREST FIRE ANALYSIS
            </p>
            <h1 className="text-4xl font-bold mt-2">
              RIMBARA
            </h1>
            <p className="text-slate-400 mt-1">
              Forest Fire Monitoring System
            </p>
          </div>

          <div className="border border-slate-700 rounded-lg px-4 py-2">
            {data ? (
              <span className="text-emerald-400">
                ● SYSTEM ONLINE
              </span>
            ) : (
              <span className="text-amber-400">
                ● {error || "CONNECTING"}
              </span>
            )}
          </div>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {[
            ["Wilayah", "Indonesia"],
            ["Satelit", "Sentinel-2"],
            ["Metode", "dNBR"]
          ].map(([label, value]) => (
            <div
              key={label}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5"
            >
              <p className="text-slate-400 text-sm">{label}</p>
              <h2 className="text-xl font-semibold mt-2">{value}</h2>
            </div>
          ))}
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="mb-5">
            <h2 className="text-xl font-bold">
              Peta Monitoring Kebakaran Hutan
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              Cakupan wilayah nasional Indonesia
            </p>
          </div>

          <IndonesiaMap />
        </section>

        <footer className="text-center text-slate-500 text-xs mt-8">
          RIMBARA © 2026 | Sentinel-2 | dNBR Analysis
        </footer>

      </div>
    </main>
  );
}
