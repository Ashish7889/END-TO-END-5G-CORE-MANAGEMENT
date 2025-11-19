const baseUrlInput = document.getElementById('baseUrl');
const apiKeyInput = document.getElementById('apiKey');
const refreshBtn = document.getElementById('refreshBtn');

// Default API base URL
if (baseUrlInput) {
  baseUrlInput.value = 'http://localhost:8009/mgmt';
}
if (apiKeyInput) {
  apiKeyInput.value = 'super-secret-admin-key';
}

const endpoints = {
  overview: '/overview',
  ues: '/ues',
  sessions: '/sessions',
  nfs: '/nfs-status',
  slices: '/slices',
  heartbeat: '/nfs/heartbeat',
  logs: {
    amf: '/logs/amf',
    smf: '/logs/smf',
    upf: '/logs/upf'
  },
  timeline: '/sessions/timeline',
  alerts: '/alerts'
};

refreshBtn?.addEventListener('click', async () => {
  // Add loading state to button
  refreshBtn.textContent = 'Refreshing...';
  refreshBtn.disabled = true;
  refreshBtn.style.opacity = '0.7';
  
  try {
    await refreshAll();
    // Show success feedback
    refreshBtn.textContent = 'Refreshed ✓';
    setTimeout(() => {
      refreshBtn.textContent = 'Refresh';
      refreshBtn.disabled = false;
      refreshBtn.style.opacity = '1';
    }, 1000);
  } catch (error) {
    console.error('Refresh failed:', error);
    // Show error feedback
    refreshBtn.textContent = 'Refresh Failed';
    setTimeout(() => {
      refreshBtn.textContent = 'Refresh';
      refreshBtn.disabled = false;
      refreshBtn.style.opacity = '1';
    }, 2000);
  }
});

document.querySelectorAll('button[data-target]').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.getAttribute('data-target');
    if (target === 'ues') loadUEs();
    if (target === 'sessions') loadSessions();
    if (target === 'nfs') loadNFs();
    if (target === 'slices') loadSlices();
  });
});

// Configuration for GitHub Pages deployment
const PRODUCTION_API_URL = 'https://5g-core-api.herokuapp.com'; // Replace with your deployed backend URL
const DEMO_MODE = true; // Set to false when backend is deployed

// Initialize API URL based on environment
function getApiUrl() {
  if (DEMO_MODE) {
    // Use mock data for demo mode
    return null;
  }
  return PRODUCTION_API_URL;
}

// Mock data generators for demo mode
const mockData = {
  overview: () => ({
    total_ues: 42,
    active_sessions: 38,
    total_sessions: 156,
    total_nfs: 7,
    active_nfs: 6,
    total_slices: 3,
    active_slices: 3,
    cpu_usage: 45.2,
    memory_usage: 62.8,
    network_throughput: 1250.5
  }),
  ues: () => ({
    ues: Array.from({length: 10}, (_, i) => ({
      ue_id: `imsi-00101000000${i}`,
      status: ['connected', 'idle', 'disconnected'][Math.floor(Math.random() * 3)],
      slice: ['eMBB', 'URLLC', 'mMTC'][Math.floor(Math.random() * 3)],
      cell_id: `cell-${Math.floor(Math.random() * 10) + 1}`,
      last_seen: new Date(Date.now() - Math.random() * 300000).toISOString()
    }))
  }),
  sessions: () => ({
    sessions: Array.from({length: 15}, (_, i) => ({
      session_id: `session-${Math.random().toString(36).substr(2, 9)}`,
      ue_id: `imsi-0010100000${Math.floor(Math.random() * 10)}`,
      slice: ['eMBB', 'URLLC', 'mMTC'][Math.floor(Math.random() * 3)],
      qos: ['Standard', 'Premium', 'Low'][Math.floor(Math.random() * 3)],
      start_time: new Date(Date.now() - Math.random() * 3600000).toISOString(),
      duration: Math.floor(Math.random() * 3600),
      bytes_up: Math.floor(Math.random() * 1000000),
      bytes_down: Math.floor(Math.random() * 5000000)
    }))
  }),
  nfs: () => ({
    nfs: ['AMF', 'SMF', 'UPF', 'AUSF', 'UDM', 'NRF', 'NSSF'].map(name => ({
      name,
      status: Math.random() > 0.2 ? 'UP' : 'DOWN',
      cpu_usage: Math.random() * 80,
      memory_usage: Math.random() * 90,
      endpoint: `192.168.1.${Math.floor(Math.random() * 255)}:8080`
    }))
  }),
  slices: () => ({
    slices: ['eMBB', 'URLLC', 'mMTC'].map(slice => ({
      slice_type: slice,
      active_ues: Math.floor(Math.random() * 20),
      total_sessions: Math.floor(Math.random() * 50),
      avg_throughput: Math.random() * 1000,
      latency: Math.random() * 50
    }))
  }),
  heartbeat: () => ({
    heartbeats: ['AMF', 'SMF', 'UPF', 'AUSF', 'UDM', 'NRF', 'NSSF'].map(name => ({
      name,
      type: name,
      status: ['UP', 'DOWN', 'UNREACHABLE'][Math.floor(Math.random() * 3)],
      endpoint: `192.168.1.${Math.floor(Math.random() * 255)}:8080`,
      last_heartbeat: new Date(Date.now() - Math.random() * 60000).toISOString()
    }))
  }),
  logs: (type) => ({
    logs: Array.from({length: 50}, (_, i) => ({
      timestamp: new Date(Date.now() - i * 10000).toISOString(),
      level: ['INFO', 'WARNING', 'ERROR'][Math.floor(Math.random() * 3)],
      message: `[${type}] ${['Session established', 'Authentication successful', 'Slice allocation', 'QoS update', 'Connection timeout', 'Resource allocation'][Math.floor(Math.random() * 6)]} for UE imsi-0010100000${Math.floor(Math.random() * 10)}`
    }))
  }),
  timeline: () => ({
    sessions: Array.from({length: 10}, (_, i) => ({
      session_id: `session-${Math.random().toString(36).substr(2, 9)}`,
      ue_id: `imsi-0010100000${Math.floor(Math.random() * 10)}`,
      slice: ['eMBB', 'URLLC', 'mMTC'][Math.floor(Math.random() * 3)],
      qos: ['Standard', 'Premium', 'Low'][Math.floor(Math.random() * 3)],
      start: new Date(Date.now() - Math.random() * 3600000).toISOString(),
      end: Math.random() > 0.5 ? new Date(Date.now() - Math.random() * 1800000).toISOString() : null
    }))
  }),
  alerts: () => ({
    alerts: Array.from({length: 8}, (_, i) => ({
      id: `alert-${Math.random().toString(36).substr(2, 9)}`,
      severity: ['critical', 'warning', 'info'][Math.floor(Math.random() * 3)],
      type: ['UE_DETACHED', 'UPF_FAILURE', 'HIGH_LATENCY', 'HIGH_BYTES', 'NF_UNREACHABLE'][Math.floor(Math.random() * 5)],
      message: [
        'UE imsi-0010100000X detached from network',
        'UPF node upf-1 experiencing high CPU usage',
        'High latency detected on slice eMBB',
        'UE imsi-0010100000X exceeded data usage limit',
        'Network function AMF unreachable'
      ][Math.floor(Math.random() * 5)],
      timestamp: new Date(Date.now() - Math.random() * 300000).toISOString()
    }))
  })
};

// Modified request function for demo mode
async function request(endpoint) {
  if (DEMO_MODE) {
    // Return mock data for demo
    await new Promise(resolve => setTimeout(resolve, 100)); // Simulate network delay
    
    if (endpoint === endpoints.overview) return mockData.overview();
    if (endpoint === endpoints.ues) return mockData.ues();
    if (endpoint === endpoints.sessions) return mockData.sessions();
    if (endpoint === endpoints.nfs) return mockData.nfs();
    if (endpoint === endpoints.slices) return mockData.slices();
    if (endpoint === endpoints.heartbeat) return mockData.heartbeat();
    if (endpoint === endpoints.logs.amf) return mockData.logs('amf');
    if (endpoint === endpoints.logs.smf) return mockData.logs('smf');
    if (endpoint === endpoints.logs.upf) return mockData.logs('upf');
    if (endpoint === endpoints.timeline) return mockData.timeline();
    if (endpoint === endpoints.alerts) return mockData.alerts();
    
    return {};
  }
  
  const baseUrl = getApiUrl();
  if (!baseUrl) {
    throw new Error('Backend API URL not configured');
  }
  
  // Original API request logic for production
  const timestamp = Date.now();
  const url = `${baseUrl}${endpoint}${endpoint.includes('?') ? '&' : '?'}_t=${timestamp}`;
  console.log('Fetching:', url);
  
  const response = await fetch(url, {
    headers: {
      'X-API-Key': 'demo-key',
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    },
  });
  
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return await response.json();
}

// Chart instances
let metricsChart = null;
let sessionChart = null;
let nfChart = null;

// Data storage for time series
const maxDataPoints = 20;
const timeLabels = [];
const ueData = [];
const sessionData = [];

// Initialize charts
function initCharts() {
  // Common chart options for premium styling
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 750,
      easing: 'easeInOutQuart'
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          font: {
            family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            size: 12,
            weight: '500'
          },
          usePointStyle: true,
          padding: 20
        }
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(59, 130, 246, 0.5)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        titleFont: {
          family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          size: 14,
          weight: '600'
        },
        bodyFont: {
          family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          size: 13
        }
      }
    }
  };

  // Create gradient definitions
  const createGradient = (ctx, color1, color2) => {
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
  };

  // Metrics line chart with premium styling
  const metricsCtx = document.getElementById('metricsChart').getContext('2d');
  const metricsGradient1 = createGradient(metricsCtx, 'rgba(59, 130, 246, 0.8)', 'rgba(59, 130, 246, 0.1)');
  const metricsGradient2 = createGradient(metricsCtx, 'rgba(168, 85, 247, 0.8)', 'rgba(168, 85, 247, 0.1)');
  
  metricsChart = new Chart(metricsCtx, {
    type: 'line',
    data: {
      labels: timeLabels,
      datasets: [
        {
          label: 'Total UEs',
          data: ueData,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: metricsGradient1,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: 'rgb(59, 130, 246)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(59, 130, 246)',
          pointHoverBorderWidth: 3
        },
        {
          label: 'Total Sessions',
          data: sessionData,
          borderColor: 'rgb(168, 85, 247)',
          backgroundColor: metricsGradient2,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: 'rgb(168, 85, 247)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(168, 85, 247)',
          pointHoverBorderWidth: 3
        }
      ]
    },
    options: {
      ...commonOptions,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(229, 231, 235, 0.5)',
            drawBorder: false
          },
          ticks: {
            font: {
              family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
              size: 11,
              weight: '500'
            },
            color: '#6b7280',
            padding: 10
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            font: {
              family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
              size: 11,
              weight: '500'
            },
            color: '#6b7280',
            padding: 10
          }
        }
      }
    }
  });

  // Session distribution doughnut chart with premium styling
  const sessionCtx = document.getElementById('sessionChart').getContext('2d');
  sessionChart = new Chart(sessionCtx, {
    type: 'doughnut',
    data: {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: [
          'rgba(59, 130, 246, 0.9)',
          'rgba(168, 85, 247, 0.9)',
          'rgba(34, 197, 94, 0.9)',
          'rgba(251, 146, 60, 0.9)',
          'rgba(239, 68, 68, 0.9)'
        ],
        borderColor: '#fff',
        borderWidth: 3,
        hoverOffset: 8,
        hoverBorderWidth: 4,
        borderRadius: 4
      }]
    },
    options: {
      ...commonOptions,
      cutout: '65%',
      plugins: {
        ...commonOptions.plugins,
        legend: {
          ...commonOptions.plugins.legend,
          position: 'bottom'
        }
      }
    }
  });

  // NF status bar chart with premium styling
  const nfCtx = document.getElementById('nfChart').getContext('2d');
  const nfGradient1 = createGradient(nfCtx, 'rgba(34, 197, 94, 0.9)', 'rgba(34, 197, 94, 0.6)');
  const nfGradient2 = createGradient(nfCtx, 'rgba(239, 68, 68, 0.9)', 'rgba(239, 68, 68, 0.6)');
  
  nfChart = new Chart(nfCtx, {
    type: 'bar',
    data: {
      labels: ['UP', 'DOWN'],
      datasets: [{
        label: 'Network Functions',
        data: [0, 0],
        backgroundColor: [nfGradient1, nfGradient2],
        borderColor: ['rgb(34, 197, 94)', 'rgb(239, 68, 68)'],
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
        maxBarThickness: 80
      }]
    },
    options: {
      ...commonOptions,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(229, 231, 235, 0.5)',
            drawBorder: false
          },
          ticks: {
            font: {
              family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
              size: 11,
              weight: '600'
            },
            color: '#6b7280',
            padding: 10,
            stepSize: 1
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            font: {
              family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
              size: 12,
              weight: '600'
            },
            color: '#374151',
            padding: 10
          }
        }
      },
      plugins: {
        ...commonOptions.plugins,
        legend: {
          display: false
        }
      }
    }
  });
}

// Update charts with new data
function updateCharts(data) {
  const now = new Date().toLocaleTimeString();
  
  // Update time series data
  if (timeLabels.length >= maxDataPoints) {
    timeLabels.shift();
    ueData.shift();
    sessionData.shift();
  }
  
  timeLabels.push(now);
  ueData.push(data.total_ues);
  sessionData.push(data.total_sessions);
  
  // Update metrics chart
  if (metricsChart) {
    metricsChart.data.labels = timeLabels;
    metricsChart.data.datasets[0].data = ueData;
    metricsChart.data.datasets[1].data = sessionData;
    metricsChart.update('none'); // Update without animation for real-time
  }
  
  // Update session distribution chart
  if (sessionChart && data.slice_distribution) {
    const sliceLabels = data.slice_distribution.map(s => `Slice ${s.slice_id}`);
    const sliceCounts = data.slice_distribution.map(s => s.session_count);
    
    sessionChart.data.labels = sliceLabels;
    sessionChart.data.datasets[0].data = sliceCounts;
    sessionChart.update('none');
  }
  
  // Update NF status chart
  if (nfChart && data.nf_status) {
    nfChart.data.datasets[0].data = [data.nf_status.up, data.nf_status.down];
    nfChart.update('none');
  }
}

async function loadOverview() {
  try {
    const data = await request(endpoints.overview);
    setText('totalUes', data.total_ues);
    setText('registeredUes', data.registered_ues);
    setText('totalSessions', data.total_sessions);
    setText('activeSessions', data.active_sessions);

    const sliceList = document.getElementById('sliceDistribution');
    sliceList.innerHTML = '';
    data.slice_distribution.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = `Slice ${item.slice_id}: ${item.session_count} sessions`;
      sliceList.appendChild(li);
    });

    const nfList = document.getElementById('nfStatus');
    nfList.innerHTML = '';
    nfList.innerHTML = `
      <li>Total: ${data.nf_status.total}</li>
      <li>UP: ${data.nf_status.up}</li>
      <li>DOWN: ${data.nf_status.down}</li>`;

    document.getElementById('upfMetrics').textContent = JSON.stringify(data.upf_metrics, null, 2);
    
    // Update charts with new data
    updateCharts(data);
  } catch (error) {
    console.error('Failed to load overview:', error);
    setText('totalUes', 'Error');
    setText('registeredUes', 'Error');
    setText('totalSessions', 'Error');
    setText('activeSessions', 'Error');
    alert(`Failed to load overview: ${error.message}`);
  }
}

async function loadUEs() {
  try {
    const ues = await request(endpoints.ues);
    const tbody = document.querySelector('#uesTable tbody');
    tbody.innerHTML = '';
    
    if (ues.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = '<td colspan="5" style="text-align: center;">No UEs registered</td>';
      tbody.appendChild(row);
    } else {
      ues.forEach((ue) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${ue.ue_id}</td>
        <td>${ue.imsi}</td>
        <td>${ue.state}</td>
        <td>${ue.slice_id ?? '-'}</td>
        <td>${new Date(ue.last_seen).toLocaleString()}</td>
      `;
        tbody.appendChild(row);
      });
    }
  } catch (err) {
    console.error(err);
    alert(`Failed to load UEs: ${err.message}`);
  }
}

async function loadSessions() {
  try {
    const sessions = await request(endpoints.sessions);
    const tbody = document.querySelector('#sessionsTable tbody');
    tbody.innerHTML = '';
    
    if (sessions.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = '<td colspan="4" style="text-align: center;">No active sessions</td>';
      tbody.appendChild(row);
    } else {
      sessions.forEach((session) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${session.id}</td>
        <td>${session.ue_id}</td>
        <td>${session.slice_id}</td>
        <td>${session.status}</td>
      `;
        tbody.appendChild(row);
      });
    }
  } catch (err) {
    console.error(err);
    alert(`Failed to load sessions: ${err.message}`);
  }
}

async function loadNFs() {
  try {
    const res = await request(endpoints.nfs);
    const nfs = res.nfs;
    const tbody = document.querySelector('#nfsTable tbody');
    tbody.innerHTML = '';
    
    if (!nfs || nfs.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = '<td colspan="3" style="text-align: center;">No Network Functions registered</td>';
      tbody.appendChild(row);
    } else {
      nfs.forEach((nf) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${nf.nf_type}</td>
        <td>${nf.name}</td>
        <td>${nf.status}</td>
      `;
        tbody.appendChild(row);
      });
    }
  } catch (err) {
    console.error(err);
    alert(`Failed to load NFs: ${err.message}`);
  }
}

async function loadSlices() {
  try {
    const slices = await request(endpoints.slices);
    const tbody = document.querySelector('#slicesTable tbody');
    tbody.innerHTML = '';
    
    if (slices.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = '<td colspan="3" style="text-align: center;">No network slices configured</td>';
      tbody.appendChild(row);
    } else {
      slices.forEach((slice) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${slice.slice_id}</td>
        <td>${slice.session_count}</td>
        <td>${slice.active_sessions}</td>
      `;
        tbody.appendChild(row);
      });
    }
  } catch (err) {
    console.error(err);
    alert(`Failed to load slices: ${err.message}`);
  }
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  // Initialize everything on page load
  document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts first
    initCharts();
    
    // Load initial data
    refreshAll();
    
    // Auto-refresh every 5 seconds for smoother real-time updates
    setInterval(refreshAll, 5000);
  });

  // Refresh all data
async function refreshAll() {
  // Add loading state to graph containers
  document.querySelectorAll('.graph-container').forEach(container => {
    container.classList.add('loading');
  });
  
  try {
    await Promise.all([
      loadOverview(),
      loadUEs(),
      loadSessions(),
      loadNFs(),
      loadSlices(),
      loadHeartbeat(),
      loadLogs('amf'),
      loadTimeline(),
      loadAlerts()
    ]);
  } finally {
    // Remove loading state
    document.querySelectorAll('.graph-container').forEach(container => {
      container.classList.remove('loading');
    });
  }
}

// NF Heartbeat Table
async function loadHeartbeat() {
  try {
    const data = await request(endpoints.heartbeat);
    const tbody = document.querySelector('#heartbeatTable tbody');
    tbody.innerHTML = '';
    
    if (data.heartbeats.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = '<td colspan="5" style="text-align: center;">No heartbeat data available</td>';
      tbody.appendChild(row);
    } else {
      data.heartbeats.forEach((nf) => {
        const row = document.createElement('tr');
        const statusClass = nf.status.toLowerCase();
        const lastHeartbeat = new Date(nf.last_heartbeat).toLocaleString();
        
        row.innerHTML = `
          <td>
            <div class="status-indicator">
              <span class="status-dot ${statusClass}"></span>
              <span>${nf.status}</span>
            </div>
          </td>
          <td>${nf.name}</td>
          <td>${nf.type}</td>
          <td>${nf.endpoint}</td>
          <td>${lastHeartbeat}</td>
        `;
        tbody.appendChild(row);
      });
    }
  } catch (err) {
    console.error('Failed to load heartbeat data:', err);
  }
}

// Log Viewer
async function loadLogs(type) {
  try {
    const data = await request(endpoints.logs[type]);
    const container = document.getElementById(`${type}-logs`);
    container.innerHTML = '';
    
    if (data.logs.length === 0) {
      container.innerHTML = '<div class="log-entry">No logs available</div>';
    } else {
      data.logs.forEach((log) => {
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${log.level.toLowerCase()}`;
        
        const timestamp = new Date(log.timestamp).toLocaleString();
        logEntry.innerHTML = `
          <span class="log-timestamp">${timestamp}</span>
          <span class="log-level">[${log.level}]</span>
          <span class="log-message">${log.message}</span>
        `;
        container.appendChild(logEntry);
      });
    }
  } catch (err) {
    console.error(`Failed to load ${type} logs:`, err);
  }
}

// Tab switching for logs
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.getAttribute('data-tab');
    
    // Update active button
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Update active content
    document.querySelectorAll('.log-content').forEach(content => content.classList.remove('active'));
    document.getElementById(`${tab}-logs`).classList.add('active');
    
    // Load logs for the selected tab
    loadLogs(tab);
  });
});

// PDU Session Timeline
let timelineChart = null;

async function loadTimeline() {
  try {
    const data = await request(endpoints.timeline);
    const ctx = document.getElementById('timelineChart').getContext('2d');
    
    // Prepare data for Chart.js
    const sessions = data.sessions.map(session => ({
      x: [session.start, session.end || new Date().toISOString()],
      y: session.ue_id,
      session: session
    }));
    
    if (timelineChart) {
      timelineChart.destroy();
    }
    
    timelineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        datasets: [{
          label: 'PDU Sessions',
          data: sessions,
          backgroundColor: sessions.map(s => 
            s.session.end ? 'rgba(34, 197, 94, 0.6)' : 'rgba(59, 130, 246, 0.6)'
          ),
          borderColor: sessions.map(s => 
            s.session.end ? 'rgba(34, 197, 94, 1)' : 'rgba(59, 130, 246, 1)'
          ),
          borderWidth: 2,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const session = context.raw.session;
                const duration = session.end ? 
                  new Date(session.end) - new Date(session.start) : 
                  new Date() - new Date(session.start);
                const durationMinutes = Math.floor(duration / 60000);
                
                return [
                  `Session ID: ${session.session_id}`,
                  `UE: ${session.ue_id}`,
                  `Slice: ${session.slice}`,
                  `QoS: ${session.qos}`,
                  `Duration: ${durationMinutes}m`,
                  `Status: ${session.end ? 'Completed' : 'Active'}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'minute',
              displayFormats: {
                minute: 'HH:mm'
              }
            },
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            title: {
              display: true,
              text: 'UE ID'
            }
          }
        }
      }
    });
  } catch (err) {
    console.error('Failed to load timeline:', err);
  }
}

// Alerts Panel
async function loadAlerts() {
  try {
    const data = await request(endpoints.alerts);
    const container = document.getElementById('alertsContainer');
    container.innerHTML = '';
    
    if (data.alerts.length === 0) {
      container.innerHTML = '<div style="text-align: center; padding: 20px; color: #6b7280;">No alerts</div>';
    } else {
      data.alerts.forEach((alert) => {
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item ${alert.severity}`;
        
        const timestamp = new Date(alert.timestamp).toLocaleString();
        
        alertItem.innerHTML = `
          <div class="alert-severity ${alert.severity}">${alert.severity}</div>
          <div class="alert-content">
            <div class="alert-message">${alert.message}</div>
            <div class="alert-timestamp">${timestamp}</div>
            <div class="alert-type">${alert.type}</div>
          </div>
        `;
        container.appendChild(alertItem);
      });
    }
  } catch (err) {
    console.error('Failed to load alerts:', err);
  }
}

// Auto-refresh for logs and alerts
setInterval(() => {
  const activeTab = document.querySelector('.tab-btn.active');
  if (activeTab) {
    const tab = activeTab.getAttribute('data-tab');
    loadLogs(tab);
  }
  loadAlerts();
}, 3000);
