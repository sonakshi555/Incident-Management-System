const API_BASE = "http://localhost:8000";

// 1. Fetch and Display Incidents
async function fetchIncidents() {
    try {
        const response = await fetch(`${API_BASE}/incidents`); // Ensure this endpoint exists in main.py
        const incidents = await response.json();
        const listElement = document.getElementById('incident-list');
        listElement.innerHTML = '';

        incidents.forEach(incident => {
            const div = document.createElement('div');
            div.className = `incident-card ${incident.severity}`;
            div.innerHTML = `
                <h3>${incident.component_id} [${incident.status}]</h3>
                <p>${incident.initial_message}</p>
                <small>MTTR: ${incident.mttr || 'Pending'}</small>
                <button onclick="showRcaForm(${incident.id})">Fill RCA</button>
            `;
            listElement.appendChild(div);
        });
    } catch (err) {
        console.error("Frontend Error:", err);
    }
}

// 2. Submit RCA
async function submitRca(event) {
    event.preventDefault();
    const incidentId = document.getElementById('rca-incident-id').value;
    
    const rcaData = {
        category: document.getElementById('category').value,
        fix_applied: document.getElementById('fix').value,
        prevention_steps: document.getElementById('prevention').value
    };

    try {
        const response = await fetch(`${API_BASE}/incidents/${incidentId}/close`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rcaData)
        });

        if (response.ok) {
            alert("Incident Closed Successfully!");
            fetchIncidents(); // Refresh list
        } else {
            const error = await response.json();
            alert(`Failed: ${error.detail}`);
        }
    } catch (err) {
        alert("Error connecting to backend.");
    }
}

// Initialize
setInterval(fetchIncidents, 5000); // Auto-refresh every 5s
fetchIncidents();