'use client';

import React, { useState, useEffect } from 'react';

type DrillResult = {
  id: string;
  backupId: string;
  type: string;
  status: string;
  checksumMatch: boolean;
  stateMatch: boolean;
  rto: number;
  rpo: number;
  overallPass: boolean;
  recommendation: string;
  expectedState: string;
  restoredState: string;
  summary: {
    backupCompleted: boolean;
    restoreSuccessful: boolean;
    checksumValid: boolean;
    dataValid: boolean;
    rtoMet: boolean;
    rpoMet: boolean;
    recoveryReady: boolean;
  };
};

export default function RestoreDrillDashboard() {
  const [drills, setDrills] = useState<DrillResult[]>([]);
  const [activeDrill, setActiveDrill] = useState<DrillResult | null>(null);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    // Load initial 5 sample drills on first load
    const initialSamples: DrillResult[] = [
      createMockDrill('NORMAL', 'DRL-001'),
      createMockDrill('CORRUPT', 'DRL-002'),
      createMockDrill('DUPLICATE', 'DRL-003'),
      createMockDrill('OUT_OF_ORDER', 'DRL-004'),
      createMockDrill('DELAYED', 'DRL-005'),
    ];
    setDrills(initialSamples.reverse());
    setActiveDrill(initialSamples[0]);
  }, []);

  const runDrill = (type: string) => {
    const newDrill = createMockDrill(type, `DRL-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`);
    setDrills(prev => [newDrill, ...prev]);
    setActiveDrill(newDrill);
  };

  // Metrics Calculation
  const totalDrills = drills.length;
  const successfulDrills = drills.filter(d => d.overallPass).length;
  const failedDrills = totalDrills - successfulDrills;
  const successRate = totalDrills > 0 ? ((successfulDrills / totalDrills) * 100).toFixed(1) : '0.0';
  const avgRto = totalDrills > 0 ? (drills.reduce((acc, d) => acc + d.rto, 0) / totalDrills).toFixed(2) : '0.00';

  if (!isClient) return null; // Avoid hydration mismatch

  return (
    <div className="min-h-screen bg-[#0F1115] text-[#E0E0E0] font-sans flex flex-col">
      {/* HEADER */}
      <header className="h-16 border-b border-[#2D3139] flex items-center justify-between px-6 bg-[#15171C] shrink-0">
        <div className="flex items-center gap-4">
          <div className="h-8 w-8 bg-[#3B82F6] flex items-center justify-center rounded">
            <span className="text-white font-bold text-xs">RRD</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight uppercase">Automated Restore-Readiness Drill</h1>
            <p className="text-[10px] text-gray-400 font-mono">MVP PREVIEW // NO EXTERNAL BACKEND REQUIRED</p>
          </div>
        </div>
        <div className="flex gap-8">
          <div className="text-right">
            <p className="text-[10px] uppercase text-gray-500">RTO Target</p>
            <p className="text-xs font-mono font-bold text-blue-400">60 seconds</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] uppercase text-gray-500">RPO Target</p>
            <p className="text-xs font-mono font-bold text-blue-400">30 seconds</p>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-auto p-4 flex flex-col gap-4">
        
        {/* METRICS ROW */}
        <section className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <MetricCard label="Total Drills" value={totalDrills} />
          <MetricCard label="Successful Drills" value={successfulDrills} color="text-green-400" />
          <MetricCard label="Failed Drills" value={failedDrills} color="text-red-400" />
          <MetricCard label="Successful Recovery Rate" value={`${successRate}%`} color="text-blue-400" />
          <MetricCard label="Average Recovery Time" value={`${avgRto}s`} />
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          {/* LEFT COLUMN: CONTROLS & SUMMARY */}
          <div className="lg:col-span-4 flex flex-col gap-4">
            
            {/* RUN CONTROLS */}
            <div className="bg-[#15171C] border border-[#2D3139] rounded-lg p-4">
              <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3">Run Restore Drill</h2>
              <div className="flex flex-col gap-2">
                <button onClick={() => runDrill('NORMAL')} className="bg-[#1A1D24] hover:bg-[#2D3139] border border-[#2D3139] text-left px-4 py-2 rounded flex justify-between items-center transition-colors">
                  <span className="text-xs font-semibold text-white">Normal Restore</span>
                  <span className="text-[10px] text-gray-500">Standard test</span>
                </button>
                <button onClick={() => runDrill('CORRUPT')} className="bg-[#1A1D24] hover:bg-red-900/30 border border-red-900/50 hover:border-red-500/50 text-left px-4 py-2 rounded flex justify-between items-center transition-colors">
                  <span className="text-xs font-semibold text-red-300">Corrupted Backup</span>
                  <span className="text-[10px] text-red-500/70">Inject bit-rot</span>
                </button>
                <button onClick={() => runDrill('DUPLICATE')} className="bg-[#1A1D24] hover:bg-[#2D3139] border border-[#2D3139] text-left px-4 py-2 rounded flex justify-between items-center transition-colors">
                  <span className="text-xs font-semibold text-white">Duplicate Event</span>
                  <span className="text-[10px] text-gray-500">Inject duplicate IDs</span>
                </button>
                <button onClick={() => runDrill('OUT_OF_ORDER')} className="bg-[#1A1D24] hover:bg-[#2D3139] border border-[#2D3139] text-left px-4 py-2 rounded flex justify-between items-center transition-colors">
                  <span className="text-xs font-semibold text-white">Out-of-Order Event</span>
                  <span className="text-[10px] text-gray-500">Shuffle sequence</span>
                </button>
                <button onClick={() => runDrill('DELAYED')} className="bg-[#1A1D24] hover:bg-[#2D3139] border border-[#2D3139] text-left px-4 py-2 rounded flex justify-between items-center transition-colors">
                  <span className="text-xs font-semibold text-white">Delayed Event</span>
                  <span className="text-[10px] text-gray-500">Simulate lag</span>
                </button>
              </div>
            </div>

            {/* ACTIVE DRILL SUMMARY & STATE */}
            {activeDrill && (
              <div className="bg-[#15171C] border border-[#2D3139] rounded-lg p-4 flex flex-col gap-4">
                <div>
                  <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Restore Readiness Summary</h2>
                  <div className="bg-[#0F1115] border border-[#2D3139] rounded p-3 text-[11px] font-mono grid grid-cols-2 gap-2">
                    <SummaryItem label="Backup Completed" value={activeDrill.summary.backupCompleted} />
                    <SummaryItem label="Restore Successful" value={activeDrill.summary.restoreSuccessful} />
                    <SummaryItem label="Checksum Valid" value={activeDrill.summary.checksumValid} />
                    <SummaryItem label="Data Valid" value={activeDrill.summary.dataValid} />
                    <SummaryItem label="RTO Met" value={activeDrill.summary.rtoMet} />
                    <SummaryItem label="RPO Met" value={activeDrill.summary.rpoMet} />
                    <div className="col-span-2 mt-2 pt-2 border-t border-[#2D3139] flex justify-between items-center font-bold">
                      <span className="text-gray-400 uppercase">Recovery Ready</span>
                      <span className={activeDrill.summary.recoveryReady ? 'text-green-400' : 'text-red-400'}>
                        {activeDrill.summary.recoveryReady ? 'YES' : 'NO'}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h2 className="text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-1">Recommendation</h2>
                  <div className={`p-3 rounded border text-[11px] leading-relaxed ${activeDrill.overallPass ? 'bg-green-900/20 border-green-700/30 text-green-100' : 'bg-red-900/20 border-red-700/30 text-red-100'}`}>
                    {activeDrill.recommendation}
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1">
                    <h2 className="text-[10px] font-bold uppercase tracking-wider text-gray-400">State Validation</h2>
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border ${activeDrill.stateMatch ? 'bg-green-900/40 text-green-400 border-green-700/50' : 'bg-red-900/40 text-red-400 border-red-700/50'}`}>
                      {activeDrill.stateMatch ? 'MATCH' : 'MISMATCH'}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <div className="text-[9px] text-gray-500 mb-1">EXPECTED STATE</div>
                      <pre className="bg-[#0F1115] border border-[#2D3139] p-2 rounded text-[9px] text-gray-300 overflow-x-auto">
                        {activeDrill.expectedState}
                      </pre>
                    </div>
                    <div>
                      <div className="text-[9px] text-gray-500 mb-1">RESTORED STATE</div>
                      <pre className={`bg-[#0F1115] border p-2 rounded text-[9px] overflow-x-auto ${activeDrill.stateMatch ? 'border-[#2D3139] text-gray-300' : 'border-red-900/50 text-red-300'}`}>
                        {activeDrill.restoredState}
                      </pre>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* RIGHT COLUMN: TABLE & ARCHITECTURE */}
          <div className="lg:col-span-8 flex flex-col gap-4">
            
            {/* RESULTS TABLE */}
            <div className="bg-[#15171C] border border-[#2D3139] rounded-lg overflow-hidden flex flex-col flex-1">
              <div className="bg-[#1A1D24] px-4 py-3 border-b border-[#2D3139]">
                <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400">Drill Execution Log</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead className="bg-[#1A1D24] text-[10px] uppercase text-gray-500">
                    <tr>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Drill ID</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Backup ID</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Restore Status</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Checksum</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Validation</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">RTO (s)</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">RPO (s)</th>
                      <th className="px-4 py-2 border-b border-[#2D3139] whitespace-nowrap">Result</th>
                    </tr>
                  </thead>
                  <tbody className="text-[11px] font-mono">
                    {drills.map((d) => (
                      <tr 
                        key={d.id} 
                        onClick={() => setActiveDrill(d)}
                        className={`border-b border-[#1E2229] hover:bg-[#1A1D24] cursor-pointer transition-colors ${activeDrill?.id === d.id ? 'bg-[#1A1D24] border-l-2 border-l-blue-500' : ''}`}
                      >
                        <td className="px-4 py-3">{d.id}</td>
                        <td className="px-4 py-3">{d.backupId}</td>
                        <td className="px-4 py-3">{d.status}</td>
                        <td className={`px-4 py-3 ${d.checksumMatch ? 'text-green-400' : 'text-red-400'}`}>{d.checksumMatch ? 'PASS' : 'FAIL'}</td>
                        <td className={`px-4 py-3 ${d.stateMatch ? 'text-green-400' : 'text-red-400'}`}>{d.stateMatch ? 'PASS' : 'FAIL'}</td>
                        <td className={`px-4 py-3 ${d.rto <= 60 ? 'text-gray-300' : 'text-red-400'}`}>{d.rto.toFixed(2)}s</td>
                        <td className={`px-4 py-3 ${d.rpo <= 30 ? 'text-gray-300' : 'text-red-400'}`}>{d.rpo.toFixed(2)}s</td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${d.overallPass ? 'bg-green-900/40 text-green-400 border-green-700/50' : 'bg-red-900/40 text-red-400 border-red-700/50'}`}>
                            {d.overallPass ? 'PASS' : 'FAIL'}
                          </span>
                        </td>
                      </tr>
                    ))}
                    {drills.length === 0 && (
                      <tr>
                        <td colSpan={8} className="px-4 py-8 text-center text-gray-500 text-xs">No drills recorded.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* DOCUMENTATION: ARCHITECTURE & COMPARISON */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              <div className="bg-[#15171C] border border-[#2D3139] rounded-lg p-4">
                <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3">Baseline vs Prototype</h2>
                <div className="text-[10px] space-y-3">
                  <div>
                    <h3 className="text-gray-300 font-bold mb-1 border-b border-[#2D3139] pb-1">BASELINE</h3>
                    <ul className="list-disc pl-4 text-gray-500 space-y-0.5">
                      <li>Restore completion check only</li>
                      <li>No checksum validation</li>
                      <li>No state validation</li>
                      <li>No RTO/RPO verification</li>
                      <li>No failure injection</li>
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-blue-300 font-bold mb-1 border-b border-[#2D3139] pb-1">PROTOTYPE</h3>
                    <ul className="list-disc pl-4 text-gray-300 space-y-0.5">
                      <li>Checksum & state validation</li>
                      <li>Automated RTO & RPO metrics</li>
                      <li>Failure simulation active</li>
                      <li>Duplicate & out-of-order handling</li>
                      <li>Automated plain-english recommendations</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="bg-[#15171C] border border-[#2D3139] rounded-lg p-4 flex flex-col">
                <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3">Architecture Flow</h2>
                <div className="flex-1 flex flex-col justify-between items-center text-[9px] font-mono font-bold text-gray-400">
                  <div className="px-3 py-1.5 bg-[#1A1D24] border border-[#2D3139] rounded w-full text-center">Session Simulator</div>
                  <span className="text-[#3B82F6]">↓</span>
                  <div className="px-3 py-1.5 bg-[#1A1D24] border border-[#2D3139] rounded w-full text-center">Backup Generator (w/ Checksum)</div>
                  <span className="text-[#3B82F6]">↓</span>
                  <div className="px-3 py-1.5 bg-[#1A1D24] border border-[#2D3139] rounded w-full text-center">Restore-Readiness Drill Engine</div>
                  <span className="text-[#3B82F6]">↓</span>
                  <div className="px-3 py-1.5 bg-[#1A1D24] border border-[#2D3139] rounded w-full text-center">RTO/RPO + State Validation</div>
                  <span className="text-[#3B82F6]">↓</span>
                  <div className="px-3 py-1.5 bg-[#1A1D24] border border-[#2D3139] rounded w-full text-center text-white">Dashboard Result</div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// Helper Components
function MetricCard({ label, value, color = "text-white" }: { label: string, value: string | number, color?: string }) {
  return (
    <div className="bg-[#1A1D24] border border-[#2D3139] p-4 rounded-lg flex flex-col justify-center">
      <span className="text-[10px] uppercase text-gray-500 font-semibold">{label}</span>
      <span className={`text-2xl font-mono font-bold ${color}`}>{value}</span>
    </div>
  );
}

function SummaryItem({ label, value }: { label: string, value: boolean }) {
  return (
    <div className="flex justify-between items-center border-b border-[#1E2229] pb-1">
      <span className="text-gray-500">{label}:</span>
      <span className={value ? 'text-green-400' : 'text-red-400'}>{value ? 'YES' : 'NO'}</span>
    </div>
  );
}

// Simulation Logic
function createMockDrill(type: string, id: string): DrillResult {
  const backupId = `BKP-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
  
  // Base State Gen
  const baseStateObj = {
    session_id: "S-101",
    player_id: "P-42",
    score: 1500,
    position: { x: 10, y: 20 },
    inventory: ["sword", "shield"],
    event_id: "evt-99",
    event_timestamp: new Date().toISOString(),
    sequence_number: 99
  };
  
  const expectedStr = JSON.stringify(baseStateObj, null, 2);
  let restoredStr = expectedStr;
  
  let checksumMatch = true;
  let stateMatch = true;
  let rto = (Math.random() * 15) + 5; // 5 - 20s
  let rpo = (Math.random() * 20) + 5; // 5 - 25s
  let status = "RESTORED";
  let recommendation = "";

  if (type === 'NORMAL') {
    recommendation = "Recovery succeeded. The backup was restored correctly and met the recovery targets.";
  } else if (type === 'CORRUPT') {
    checksumMatch = false;
    stateMatch = false;
    status = "ERROR";
    const corruptStateObj = { ...baseStateObj, score: -9999, inventory: [] };
    restoredStr = JSON.stringify(corruptStateObj, null, 2);
    recommendation = "Recovery failed because the backup checksum did not match. This backup should not be considered recovery-ready.";
  } else if (type === 'DUPLICATE') {
    recommendation = "Duplicate events were detected and safely ignored. Final session state remains correct.";
  } else if (type === 'OUT_OF_ORDER') {
    recommendation = "Events arrived out of order, but the final session state remained correct through sequence sorting.";
  } else if (type === 'DELAYED') {
    recommendation = "Delayed events were successfully merged into the timeline without corrupting the active state.";
  }

  const rtoPass = rto <= 60;
  const rpoPass = rpo <= 30;
  const overallPass = checksumMatch && stateMatch && rtoPass && rpoPass;

  return {
    id,
    backupId,
    type,
    status,
    checksumMatch,
    stateMatch,
    rto,
    rpo,
    overallPass,
    recommendation,
    expectedState: expectedStr,
    restoredState: restoredStr,
    summary: {
      backupCompleted: true,
      restoreSuccessful: status !== "ERROR",
      checksumValid: checksumMatch,
      dataValid: stateMatch,
      rtoMet: rtoPass,
      rpoMet: rpoPass,
      recoveryReady: overallPass
    }
  };
}
