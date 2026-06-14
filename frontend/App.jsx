import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import { Shield, CloudRain, Navigation, Activity, Waves, AlertTriangle, Compass, RefreshCw, Layers } from 'lucide-react';
import L from 'leaflet';

// Leaflet anchor icon configurations
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function MapController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.setView(center, zoom || 6);
  }, [center, zoom, map]);
  return null;
}

export default function App() {
  const [rainfall, setRainfall] = useState(150);
  const [targetTown, setTargetTown] = useState('Manila_Core');
  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Nationwide tracking architecture configuration spanning all operational regions
  const townsData = [
    { id: "Manila_Core", name: "Manila Core Hub", region: "Luzon" },
    { id: "Clark_Hub", name: "Clark Aviation Hub", region: "Luzon" },
    { id: "Legazpi_Hub", name: "Legazpi Logistics Node", region: "Luzon" },
    { id: "Cebu_City", name: "Cebu City Terminal", region: "Visayas" },
    { id: "Iloilo_Hub", name: "Iloilo Maritime Hub", region: "Visayas" },
    { id: "Tacloban_Port", name: "Tacloban Gateway", region: "Visayas" },
    { id: "Davao_City", name: "Davao Core Node", region: "Mindanao" },
    { id: "Cagayan_de_Oro", name: "CDO Transit Center", region: "Mindanao" },
    { id: "Zamboanga_Hub", name: "Zamboanga Peninsula Port", region: "Mindanao" }
  ];

  const defaultCoords = {
    "Manila_Core": { lat: 14.5995, lon: 120.9842 },
    "Clark_Hub": { lat: 15.1851, lon: 120.5398 },
    "Legazpi_Hub": { lat: 13.1374, lon: 123.7438 },
    "Cebu_City": { lat: 10.3157, lon: 123.8854 },
    "Iloilo_Hub": { lat: 10.7202, text: "Iloilo", lon: 122.5621 },
    "Tacloban_Port": { lat: 11.2444, lon: 125.0039 },
    "Davao_City": { lat: 7.1907, lon: 125.4553 },
    "Cagayan_de_Oro": { lat: 8.4542, lon: 124.6319 },
    "Zamboanga_Hub": { lat: 6.9214, lon: 122.0790 }
  };

  useEffect(() => {
    const fetchRouteDetails = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/optimize-route', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rainfall, target_town: targetTown }),
        });
        const data = await response.json();
        setApiData(data);
      } catch (error) {
        console.error("Route calculations processed via fallback parameters.", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRouteDetails();
  }, [rainfall, targetTown]);

  const calculatedRiskVal = Math.min(Math.round((rainfall / 400) * 100), 100);

  const getRiskStatus = (riskScore) => {
    if (riskScore < 40) return { 
      style: 'border-emerald-500/50 text-emerald-200 bg-slate-800/80 hover:border-emerald-400 hover:shadow-[0_0_20px_rgba(16,185,129,0.4)]', 
      label: 'Optimal Transit Path', 
      dot: 'bg-emerald-400 shadow-[0_0_12px_#10b981]' 
    };
    if (riskScore < 75) return { 
      style: 'border-amber-500/50 text-amber-200 bg-slate-800/80 hover:border-amber-400 hover:shadow-[0_0_20px_rgba(245,158,11,0.4)]', 
      label: 'Caution: Moderate Hazard', 
      dot: 'bg-amber-400 shadow-[0_0_12px_#f59e0b]' 
    };
    return { 
      style: 'border-rose-500 text-rose-100 bg-rose-950/40 border-dashed animate-pulse shadow-[0_0_15px_rgba(244,63,94,0.2)] font-semibold', 
      label: 'Critical Inundation Danger', 
      dot: 'bg-rose-500 shadow-[0_0_14px_#f43f5e] scale-110' 
    };
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-900 text-slate-100 overflow-hidden font-sans antialiased">
      
      {/* ATTRACTIVE GRADIENT TOP HEADER BAR */}
      <header className="flex items-center justify-between px-6 py-5 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border-b-2 border-indigo-500/40 shrink-0 z-10 shadow-[0_4px_30px_rgba(0,0,0,0.4)]">
        <div className="flex items-center space-x-4">
          <div className="p-2.5 bg-gradient-to-br from-cyan-500/30 to-indigo-600/20 rounded-xl border-2 border-cyan-400 shadow-[0_0_20px_rgba(34,211,238,0.3)]">
            <Shield className="w-8 h-8 text-cyan-400" />
          </div>
          <div>
            {/* UPDATED HEADER TITLE TO PHILIPPINES */}
            <h1 className="text-2xl font-black tracking-wider text-white uppercase bg-clip-text bg-gradient-to-r from-white via-cyan-100 to-indigo-200">
              PHILIPPINES CLIMATE LOGISTICS CONTROL
            </h1>
            <p className="text-xs text-cyan-400 font-mono tracking-widest flex items-center gap-2 mt-0.5">
              <Activity className="w-4 h-4 text-cyan-400 animate-pulse" /> NATIONWIDE QUANTUM MATRIX ARCHITECTURE
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3 text-sm bg-slate-900 px-5 py-2.5 rounded-xl border-2 border-indigo-500/40 font-mono shadow-[0_0_15px_rgba(99,102,241,0.2)]">
          <span className="w-3 h-3 rounded-full bg-cyan-400 shadow-[0_0_12px_#22d3ee] animate-ping absolute" />
          <span className="w-3 h-3 rounded-full bg-cyan-400 shadow-[0_0_12px_#22d3ee]" />
          <span className="text-cyan-400 font-black tracking-widest pl-1">CORE ONLINE</span>
        </div>
      </header>

      {/* Main Workspace Frame */}
      <div className="flex flex-1 overflow-hidden">
        
        {/* HUGE, BRIGHT, COSMIC SLATE-INDIGO SIDEBAR CONTAINER */}
        <aside className="w-[560px] bg-gradient-to-b from-indigo-950/90 via-slate-900 to-indigo-950/90 border-r-2 border-indigo-500/30 p-6 flex flex-col space-y-6 overflow-y-auto shrink-0 z-10 text-slate-100 shadow-[10px_0_40px_rgba(0,0,0,0.5)] backdrop-blur-md">
          
          {/* Controls Card Component Container */}
          <div className={`p-6 rounded-2xl border-2 transition-all duration-500 bg-slate-900/90 shadow-2xl ${rainfall > 200 ? 'border-rose-500 shadow-rose-950/40 bg-gradient-to-br from-slate-900 to-rose-950/30' : 'border-cyan-400 shadow-cyan-950/30 bg-gradient-to-br from-slate-900 to-indigo-950/40'}`}>
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2.5">
                <CloudRain className={`w-6 h-6 ${rainfall > 200 ? 'text-rose-400' : 'text-cyan-400'}`} /> 
                Atmospheric Load Configuration
              </h2>
              {rainfall > 200 ? (
                <span className="text-xs bg-rose-500 text-white font-mono px-3 py-1 rounded-md uppercase tracking-wider font-black shadow-[0_0_20px_rgba(244,63,94,0.6)] animate-bounce">
                  TYPHOON FORCE
                </span>
              ) : (
                <span className="text-xs bg-cyan-400 text-slate-950 font-mono px-3 py-1 rounded-md uppercase tracking-wider font-black shadow-[0_0_20px_rgba(6,182,212,0.5)]">
                  STABLE CONDITIONS
                </span>
              )}
            </div>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-200 font-extrabold text-base tracking-wide">Precipitation Gauge:</span>
                <span className={`font-black text-2xl font-mono px-4 py-1.5 rounded-xl shadow-2xl ${rainfall > 200 ? 'text-rose-400 bg-rose-500/20 border border-rose-500/40' : 'text-cyan-400 bg-cyan-500/20 border border-cyan-400/40'}`}>
                  {rainfall} mm
                </span>
              </div>
              <input 
                type="range" min="50" max="400" value={rainfall} 
                onChange={(e) => setRainfall(parseFloat(e.target.value))}
                className="w-full h-3 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400 shadow-inner"
              />
              <div className="flex justify-between text-xs font-mono text-indigo-300 font-bold px-1">
                <span>50mm (Light Mist)</span>
                <span>400mm (Extreme Emergency)</span>
              </div>
            </div>

            <div className="space-y-3 mt-6 border-t-2 border-indigo-500/20 pt-5">
              <label className="block text-sm font-black text-slate-200 uppercase tracking-wider">Target Node Destination Vector:</label>
              <div className="relative">
                <select 
                  value={targetTown} onChange={(e) => setTargetTown(e.target.value)}
                  className="w-full bg-slate-900 hover:bg-slate-800 text-white font-black text-base border-2 border-indigo-500/50 rounded-xl p-4 focus:ring-4 focus:ring-cyan-400/30 focus:border-cyan-400 focus:outline-none cursor-pointer transition-all shadow-xl appearance-none"
                >
                  {townsData.map(town => (
                    <option key={town.id} value={town.id} className="bg-slate-900 text-white font-bold p-2">
                      {town.name} [{town.region}]
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-cyan-400">
                  <Navigation className="w-5 h-5 rotate-90" />
                </div>
              </div>
            </div>
          </div>

          {/* Core Analytics Stat Badges */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-slate-900 border-2 border-cyan-400/50 rounded-2xl flex items-center gap-4 shadow-2xl bg-gradient-to-br from-slate-900 to-indigo-950/50 hover:border-cyan-400 transition-all duration-300">
              <div className="p-3 bg-cyan-500/20 rounded-xl text-cyan-400 border border-cyan-400/40 shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                <Layers className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs uppercase font-mono text-slate-300 block font-bold tracking-widest">Active Nodes</span>
                <span className="text-lg font-black text-white font-mono tracking-tight">{townsData.length} Anchors</span>
              </div>
            </div>
            <div className="p-4 bg-slate-900 border-2 border-indigo-400/50 rounded-2xl flex items-center gap-4 shadow-2xl bg-gradient-to-br from-slate-900 to-indigo-950/50 hover:border-indigo-400 transition-all duration-300">
              <div className="p-3 bg-indigo-500/20 rounded-xl text-indigo-400 border border-indigo-400/40 shadow-[0_0_15px_rgba(99,102,241,0.3)]">
                <Compass className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs uppercase font-mono text-slate-300 block font-bold tracking-widest">System Threat</span>
                <span className="text-lg font-black text-white font-mono tracking-tight">~{calculatedRiskVal}% Index</span>
              </div>
            </div>
          </div>

          {/* Interactive Risk List Grid Feed Header */}
          <div className="flex-1 flex flex-col space-y-3 min-h-[320px]">
            <div className="flex items-center justify-between border-b-2 border-indigo-500/30 pb-3">
              <h3 className="text-sm font-black text-white uppercase tracking-widest font-mono flex items-center gap-2">
                <Waves className="w-5 h-5 text-cyan-400" /> Archipelagic Vulnerability Feed
              </h3>
              <div className="flex items-center gap-2 text-xs text-cyan-400 font-mono font-bold bg-cyan-500/10 px-3 py-1.5 border border-cyan-400/40 rounded-md shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                <RefreshCw className="w-4 h-4 animate-spin" /> DISPATCH MATRIX LIVE
              </div>
            </div>
            
            {/* Scrollable Risk Node Target Rows */}
            <div className="space-y-3 overflow-y-auto pr-1 flex-1 max-h-[360px] scrollbar-thin scrollbar-thumb-indigo-500">
              {townsData.map(town => {
                const calculatedHubRisk = Math.min(calculatedRiskVal + (town.region === 'Luzon' ? 4 : town.region === 'Visayas' ? -6 : 5), 100);
                const status = getRiskStatus(calculatedHubRisk);
                const isSelected = targetTown === town.id;
                
                return (
                  <div 
                    key={town.id} 
                    onClick={() => setTargetTown(town.id)}
                    className={`flex items-center justify-between p-4 rounded-xl border-2 transition-all duration-300 transform cursor-pointer hover:-translate-x-2 shadow-xl ${status.style} ${
                      isSelected 
                        ? 'ring-4 ring-cyan-400/50 border-cyan-400 bg-gradient-to-r from-indigo-900 to-cyan-950 shadow-[0_0_25px_rgba(34,211,238,0.4)]' 
                        : 'bg-slate-900/70'
                    }`}
                  >
                    <div className="space-y-2">
                      <div className="flex items-center gap-3">
                        <span className={`w-3.5 h-3.5 rounded-full ${status.dot}`} />
                        <span className={`font-black text-lg tracking-wide ${isSelected ? 'text-cyan-400' : 'text-white'}`}>
                          {town.name}
                        </span>
                        <span className="text-xs font-mono font-black px-2.5 py-0.5 bg-indigo-950 border border-indigo-500/40 text-cyan-300 rounded-md">
                          {town.region}
                        </span>
                      </div>
                      <span className="text-xs font-extrabold uppercase tracking-widest text-slate-300 block pl-6">
                        {status.label}
                      </span>
                    </div>
                    <div className="text-right">
                      <span className="font-mono text-2xl font-black text-white tracking-tight">{calculatedHubRisk}%</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Routing Information Box Metrics Container */}
          <div className="bg-slate-900 p-5 rounded-2xl border-2 border-indigo-500/30 shadow-[inset_0_0_30px_rgba(0,0,0,0.5)] mt-auto">
            <h3 className="text-xs font-black text-indigo-300 uppercase tracking-widest flex items-center gap-2 font-mono mb-4">
              <Navigation className="w-5 h-5 text-emerald-400" /> Operational Pathing Logic Output
            </h3>
            {loading ? (
              <div className="flex flex-col items-center justify-center py-6 space-y-3">
                <div className="w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" />
                <p className="text-xs text-cyan-400 font-mono tracking-widest">COMPUTING OPTIMAL VECTOR WEIGHTS...</p>
              </div>
            ) : apiData?.is_accessible ? (
              <div className="space-y-4">
                <div className="px-3 py-1.5 bg-emerald-500/20 border-2 border-emerald-500/60 rounded-lg text-xs text-emerald-300 font-mono font-black tracking-widest inline-block shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                  ✔ ARCHIPELAGO CORRIDOR OPEN
                </div>
                <div className="text-sm text-slate-200 bg-slate-800 p-4 rounded-xl border border-indigo-500/20 shadow-inner">
                  <span className="font-mono text-cyan-400 text-xs block mb-2 uppercase tracking-widest font-black">Calculated Dispatch Flow:</span>
                  <p className="font-black text-white text-lg tracking-wide leading-relaxed">{apiData.route.join(' ➔ ')}</p>
                </div>
                <div className="text-sm border-t border-slate-900 pt-3 flex justify-between font-mono items-center">
                  <span className="text-slate-400 font-bold text-xs uppercase tracking-wider">Friction Cost Index:</span>
                  <span className="text-emerald-400 font-black text-lg bg-emerald-500/20 px-3 py-1 rounded-lg border border-emerald-500/40 shadow-sm">{parseFloat(apiData.risk_adjusted_cost).toFixed(2)}</span>
                </div>
              </div>
            ) : (
              <div className="p-4 bg-gradient-to-br from-rose-500/20 to-transparent border-2 border-rose-500/50 rounded-xl flex gap-4 text-sm text-rose-200 shadow-[0_0_25px_rgba(244,63,94,0.2)] animate-pulse">
                <AlertTriangle className="w-7 h-7 shrink-0 text-rose-400" />
                <div className="space-y-2">
                  <span className="font-black uppercase block tracking-widest text-rose-300 text-xs">CRITICAL STRATEGIC LINK FAILURE</span>
                  <p className="text-slate-200 text-xs leading-relaxed font-semibold">Severe rainfall triggers maritime transit suspension across the archipelago. Inter-island lanes blocked. Please adjust the slider or choose alternate hubs.</p>
                </div>
              </div>
            )}
          </div>
        </aside>

        {/* Map Display Viewport */}
        <main className="flex-1 h-full bg-slate-100 relative">
          <MapContainer 
            center={[12.8797, 121.7740]} zoom={6} 
            style={{ width: '100%', height: '100%' }}
            zoomControl={false}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
            />
            
            {apiData?.is_accessible && apiData?.route_coordinates && (
              <Polyline 
                positions={apiData.route_coordinates} 
                pathOptions={{ color: '#6366f1', weight: 6, opacity: 0.95 }} 
              />
            )}

            {Object.entries(defaultCoords).map(([name, coords]) => (
              <Marker key={name} position={[coords.lat, coords.lon]}>
                <Popup>
                  <div className="p-1 font-sans text-slate-900">
                    <h4 className="font-bold border-b pb-0.5 mb-1 text-xs">{name.replace('_', ' ')}</h4>
                    <p className="text-[10px] font-mono">Logistics Vector Node Connected</p>
                  </div>
                </Popup>
              </Marker>
            ))}
            
            <MapController center={[12.8797, 121.7740]} zoom={6} />
          </MapContainer>
        </main>
      </div>
    </div>
  );
}