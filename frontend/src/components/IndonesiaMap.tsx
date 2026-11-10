"use client";

import {
  MapContainer,
  TileLayer,
  ZoomControl
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

export default function IndonesiaMap() {
  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden">
      <MapContainer
        center={[-2.5, 118]}
        zoom={5}
        minZoom={4}
        maxZoom={15}
        scrollWheelZoom={true}
        zoomControl={false}
        style={{
          height: "100%",
          width: "100%"
        }}
      >
        <ZoomControl position="bottomright" />

        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>
    </div>
  );
}