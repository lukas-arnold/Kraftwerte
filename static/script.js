const API_URL = window.location.origin;

const kraftwerteTableBody = document.querySelector('#kraftwerteTable tbody');
const kraftwertForm = document.getElementById('kraftwertForm');
const muskelgruppeInput = document.getElementById('muskelgruppe');
const uebungInput = document.getElementById('uebung');
const gewichtInput = document.getElementById('gewicht');
const submitButton = document.getElementById('submitButton');
const cancelEditButton = document.getElementById('cancelEditButton');
const formTitle = document.getElementById('formTitle');
const messageDiv = document.getElementById('message');

let editingKraftwertId = null;

function showMessage(msg, type) {
    messageDiv.textContent = msg;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}

function formatDateToDay(isoTimestamp) {
    if (!isoTimestamp) return '';
    const date = new Date(isoTimestamp);
    return date.toISOString().split('T')[0];
}

async function fetchKraftwerte() {
    try {
        const response = await fetch(`${API_URL}/kraftwerte/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const kraftwerte = await response.json();
        renderKraftwerte(kraftwerte);
    } catch (error) {
        console.error("Fehler beim Abrufen der Kraftwerte:", error);
        showMessage("Fehler beim Laden der Kraftwerte. Server möglicherweise nicht erreichbar.", "error");
    }
}

function renderKraftwerte(kraftwerte) {
    kraftwerteTableBody.innerHTML = '';
    if (kraftwerte.length === 0) {
        kraftwerteTableBody.innerHTML = '<tr><td colspan="5">Noch keine Kraftwerte vorhanden.</td></tr>';
        return;
    }

    kraftwerte.forEach(kraftwert => {
        const row = kraftwerteTableBody.insertRow();

        // Jede Zelle erstellen und data-label hinzufügen
        const muskelgruppeCell = row.insertCell();
        muskelgruppeCell.textContent = kraftwert.muskelgruppe;
        muskelgruppeCell.setAttribute('data-label', 'Muskelgruppe'); // Hinzugefügt

        const uebungCell = row.insertCell();
        uebungCell.textContent = kraftwert.uebung;
        uebungCell.setAttribute('data-label', 'Übung'); // Hinzugefügt

        const gewichtCell = row.insertCell();
        gewichtCell.textContent = kraftwert.gewicht.toFixed(1);
        gewichtCell.setAttribute('data-label', 'Gewicht (kg)'); // Hinzugefügt

        const updatedAtCell = row.insertCell();
        updatedAtCell.textContent = formatDateToDay(kraftwert.updated_at);
        updatedAtCell.setAttribute('data-label', 'Zuletzt geändert'); // Hinzugefügt

        const actionsCell = row.insertCell();
        actionsCell.className = 'actions';
        actionsCell.setAttribute('data-label', 'Aktionen'); // Hinzugefügt

        const editButton = document.createElement('button');
        editButton.textContent = 'Bearbeiten';
        editButton.className = 'edit-btn';
        editButton.onclick = () => loadKraftwertForEdit(kraftwert.id);
        actionsCell.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Löschen';
        deleteButton.onclick = () => deleteKraftwert(kraftwert.id);
        actionsCell.appendChild(deleteButton);
    });
}

async function loadKraftwertForEdit(id) {
    try {
        const response = await fetch(`${API_URL}/kraftwerte/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const kraftwert = await response.json();

        muskelgruppeInput.value = kraftwert.muskelgruppe;
        uebungInput.value = kraftwert.uebung;
        gewichtInput.value = kraftwert.gewicht;
        editingKraftwertId = kraftwert.id;

        submitButton.textContent = 'Aktualisieren';
        formTitle.textContent = 'Kraftwert bearbeiten';
        cancelEditButton.style.display = 'inline-block';

        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        console.error("Fehler beim Laden des Kraftwerts zum Bearbeiten:", error);
        showMessage("Fehler beim Laden des Kraftwerts zum Bearbeiten.", "error");
    }
}

function resetForm() {
    kraftwertForm.reset();
    submitButton.textContent = 'Hinzufügen';
    formTitle.textContent = 'Neuen Kraftwert hinzufügen';
    cancelEditButton.style.display = 'none';
    editingKraftwertId = null;
}

kraftwertForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const muskelgruppe = muskelgruppeInput.value;
    const uebung = uebungInput.value;
    const gewicht = parseFloat(gewichtInput.value);

    if (isNaN(gewicht)) {
        showMessage("Bitte ein gültiges Gewicht eingeben.", "error");
        return;
    }

    const data = { muskelgruppe, uebung, gewicht };

    try {
        let response;
        if (editingKraftwertId) {
            response = await fetch(`${API_URL}/kraftwerte/${editingKraftwertId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
        } else {
            response = await fetch(`${API_URL}/kraftwerte/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
        }

        if (response.ok || response.status === 201) {
            showMessage(`Kraftwert erfolgreich ${editingKraftwertId ? 'aktualisiert' : 'hinzugefügt'}!`, "success");
            resetForm();
            fetchKraftwerte();
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Fehler beim ${editingKraftwertId ? 'Aktualisieren' : 'Hinzufügen'}: ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Fehler bei der Operation (${editingKraftwertId ? 'Aktualisieren' : 'Hinzufügen'}):`, error);
        showMessage(`Fehler: ${error.message}`, "error");
    }
});

cancelEditButton.addEventListener('click', resetForm);

async function deleteKraftwert(id) {
    if (!confirm(`Soll der Kraftwert mit ID ${id} wirklich gelöscht werden?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/kraftwerte/${id}`, {
            method: 'DELETE',
        });

        if (response.status === 204) {
            showMessage("Kraftwert erfolgreich gelöscht!", "success");
            fetchKraftwerte();
            if (editingKraftwertId === id) {
                resetForm();
            }
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Fehler beim Löschen: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Fehler beim Löschen des Kraftwerts:", error);
        showMessage(`Fehler: ${error.message}`, "error");
    }
}

document.addEventListener('DOMContentLoaded', fetchKraftwerte);
