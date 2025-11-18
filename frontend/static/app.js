const baseUrlInput = document.getElementById('baseUrl');
const apiKeyInput = document.getElementById('apiKey');
const refreshBtn = document.getElementById('refreshBtn');

const endpoints = {
  overview: '/overview',
  ues: '/ues',
  sessions: '/sessions',
  nfs: '/nfs-status'
};

refreshBtn?.addEventListener('click', () => {
  refreshAll();
});

document.querySelectorAll('button[data-target]').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.getAttribute('data-target');
    if (target === 'ues') loadUEs();
    if (target === 'sessions') loadSessions();
    if (target === 'nfs') loadNFs();
  });
});

async function request(endpoint) {
  const baseUrl = baseUrlInput.value.replace(/\/$/, '');
  const url = `${baseUrl}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'X-API-Key': apiKeyInput.value,
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Request failed: ${response.status} - ${text}`);
  }
  return response.json();
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
      li.textContent = `${item.slice_id}: ${item.session_count}`;
      sliceList.appendChild(li);
    });

    const nfList = document.getElementById('nfStatus');
    nfList.innerHTML = '';
    nfList.innerHTML = `
      <li>Total: ${data.nf_status.total}</li>
      <li>UP: ${data.nf_status.up}</li>
      <li>DOWN: ${data.nf_status.down}</li>`;

    document.getElementById('upfMetrics').textContent = JSON.stringify(data.upf_metrics, null, 2);
  } catch (err) {
    console.error(err);
    alert(`Failed to load overview: ${err.message}`);
  }
}

async function loadUEs() {
  try {
    const ues = await request(endpoints.ues);
    const tbody = document.querySelector('#uesTable tbody');
    tbody.innerHTML = '';
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
    sessions.forEach((session) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${session.id}</td>
        <td>${session.ue_id}</td>
        <td>${session.slice_id}</td>
        <td>${session.status}</td>
        <td>${session.upf_session_id ?? '-'}</td>
      `;
      tbody.appendChild(row);
    });
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
    nfs.forEach((nf) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${nf.nf_type}</td>
        <td>${nf.name}</td>
        <td class="${nf.status === 'UP' ? 'status-up' : 'status-down'}">${nf.status}</td>
        <td>${nf.endpoint}</td>
        <td>${new Date(nf.last_heartbeat).toLocaleString()}</td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error(err);
    alert(`Failed to load NF status: ${err.message}`);
  }
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function refreshAll() {
  loadOverview();
  loadUEs();
  loadSessions();
  loadNFs();
}

refreshAll();
setInterval(refreshAll, 10000);
