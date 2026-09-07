document.addEventListener('DOMContentLoaded', () => {
    fetchResults();
    setInterval(updateTick, 1000);
    updateTick();
});

function updateTick() {
    const el = document.getElementById('system-tick');
    if (el) {
        el.textContent = `SYSTEM_TICK: ${new Date().toISOString()}`;
    }
}

async function fetchResults() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();
        
        renderMetrics(data.metrics);
        renderTable(data.results);
        renderRecommendations(data.results);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function renderMetrics(metrics) {
    const container = document.getElementById('metrics-cards');
    if (!metrics || Object.keys(metrics).length === 0) {
        container.innerHTML = '<p class="text-gray-400 p-4">No drill data available. Please run the experiment script.</p>';
        return;
    }

    const cards = [
        { label: 'Total Drills', value: metrics.total_drills, valClass: 'text-white' },
        { label: 'Successful', value: metrics.successful_drills, valClass: 'text-green-400' },
        { label: 'Failed', value: metrics.failed_drills, valClass: 'text-red-500' },
        { label: 'Success Rate', value: `${metrics.recovery_success_rate}%`, valClass: 'text-blue-400' },
        { label: 'Avg RTO', value: `${metrics.average_recovery_time}s`, valClass: 'text-white' }
    ];

    container.innerHTML = cards.map(c => `
        <div class="bg-[#1A1D24] border border-[#2D3139] p-4 rounded-lg flex flex-col justify-center">
            <span class="text-[10px] uppercase text-gray-500 font-semibold">${c.label}</span>
            <span class="text-3xl font-mono font-bold ${c.valClass}">${c.value}</span>
        </div>
    `).join('');
}

function renderTable(results) {
    const tbody = document.querySelector('#results-table tbody');
    tbody.innerHTML = results.map(r => {
        const overallPass = r.overall_result === 'PASS';
        const checksumPass = r.checksum_match;
        const validationPass = r.state_match;
        
        return `
        <tr class="border-b border-[#1E2229] hover:bg-[#1A1D24]">
            <td class="px-4 py-3">${r.drill_id.substring(0, 8)}</td>
            <td class="px-4 py-3">${r.backup_id.substring(0, 8)}</td>
            <td class="px-4 py-3 ${overallPass ? 'text-green-400' : 'text-red-400'}">${r.overall_result !== "FAIL" ? "RESTORED" : "ERROR"}</td>
            <td class="px-4 py-3 ${checksumPass ? 'text-green-400' : 'text-red-400'}">${checksumPass ? 'MATCH' : 'MISMATCH'}</td>
            <td class="px-4 py-3 ${validationPass ? 'text-green-400' : 'text-red-400'}">${validationPass ? 'PASS' : 'FAIL'}</td>
            <td class="px-4 py-3">${r.actual_rto.toFixed(2)}s</td>
            <td class="px-4 py-3">${r.actual_rpo.toFixed(2)}s</td>
            <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded border text-[10px] font-bold ${overallPass ? 'bg-green-900/40 text-green-400 border-green-700/50' : 'bg-red-900/40 text-red-400 border-red-700/50'}">
                    ${r.overall_result}
                </span>
            </td>
        </tr>
    `}).join('');
}

function renderRecommendations(results) {
    const list = document.getElementById('recommendations-list');
    
    // Group recommendations to avoid duplicates
    const uniqueRecs = new Set(results.map(r => r.recommendation));
    
    list.innerHTML = Array.from(uniqueRecs).map(rec => {
        const isError = rec.toLowerCase().includes('fail') || rec.toLowerCase().includes('corrupt') || rec.toLowerCase().includes('exceed');
        
        return `
        <div class="p-3 rounded-lg border ${isError ? 'bg-red-900/20 border-red-500/30' : 'bg-blue-900/20 border-blue-500/30'}">
            <h3 class="text-[10px] font-bold uppercase mb-1 ${isError ? 'text-red-300' : 'text-blue-300'}">System Insight</h3>
            <p class="text-[11px] leading-relaxed italic ${isError ? 'text-red-100' : 'text-blue-100'}">
                "${rec}"
            </p>
        </div>
    `}).join('');
}
