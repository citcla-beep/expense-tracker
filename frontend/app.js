// URL base del tuo backend
const API_URL = "http://localhost:8000"

// Recupera mese e anno corrente
const oggi = new Date()
const mese = oggi.getMonth() + 1  // getMonth() parte da 0, quindi aggiungi 1
const anno = oggi.getFullYear()

// Gestisce la navigazione tra sezioni
function mostraSezione(nomeSezione) {
    // Rimuove "active" da tutte le sezioni e bottoni
    document.querySelectorAll(".sezione").forEach(s => s.classList.remove("active"))
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"))

    // Aggiunge "active" alla sezione e bottone corretti
    document.getElementById(nomeSezione).classList.add("active")
    document.querySelector(`[onclick="mostraSezione('${nomeSezione}')"]`).classList.add("active")
}

async function caricaDashboard() {
    try {
        const response = await fetch(`${API_URL}/api/riepilogo?mese=${mese}&anno=${anno}`)
        const dati = await response.json()

        document.getElementById("totale-entrate").textContent = `€${dati.totale_entrate.toFixed(2)}`
        document.getElementById("totale-spese").textContent = `€${dati.totale_spese.toFixed(2)}`

        // Saldo — aggiunge classe positivo o negativo dinamicamente
        const saldoEl = document.getElementById("saldo")
        saldoEl.textContent = `€${dati.saldo.toFixed(2)}`
        saldoEl.classList.remove("positivo", "negativo")
        saldoEl.classList.add(dati.saldo >= 0 ? "positivo" : "negativo")

        // Spese pianificate
        const pianoResponse = await fetch(`${API_URL}/api/riepilogo/spese-pianificate`)
        const pianoDati = await pianoResponse.json()
        document.getElementById("spese-pianificate").textContent = `€${pianoDati.totale_spese_pianificate.toFixed(2)}`

    } catch (error) {
        console.error("Errore nel caricamento della dashboard:", error)
    }
}
async function caricaSpese(filtri = {}) {
    try {
        // Costruisce i query parameters solo per i filtri non vuoti
        const params = new URLSearchParams()
        if (filtri.categoria)    params.append("categoria", filtri.categoria)
        if (filtri.data_inizio)  params.append("data_inizio", filtri.data_inizio)
        if (filtri.data_fine)    params.append("data_fine", filtri.data_fine)
        if (filtri.descrizione)  params.append("descrizione", filtri.descrizione)

        const url = `${API_URL}/api/spese${params.toString() ? "?" + params.toString() : ""}`
        const response = await fetch(url)
        const spese = await response.json()
        const lista = document.getElementById("lista-spese")

        if (spese.length === 0) {
            lista.innerHTML = `<p class="empty-state">Nessuna spesa trovata</p>`
            return
        }

        lista.innerHTML = spese.map(spesa => `
            <li class="list-item">
                <div class="list-item-info">
                    <p class="list-item-nome">${spesa.categoria}</p>
                    <p class="list-item-sub">${spesa.data} ${spesa.descrizione ? "· " + spesa.descrizione : ""}</p>
                </div>
                <span class="badge ${spesa.tipo === 'pianificata' ? 'badge-pianificata' : ''}">
                    ${spesa.tipo}
                </span>
                <span class="list-item-importo negativo">-€${spesa.importo.toFixed(2)}</span>
                <button class="btn-delete" onclick="eliminaSpesa(${spesa.id})">✕</button>
            </li>
        `).join("")

    } catch (error) {
        console.error("Errore nel caricamento delle spese:", error)
    }
}

function cercaSpese() {
    caricaSpese({
        categoria:   document.getElementById("filtro-categoria").value,
        data_inizio: document.getElementById("filtro-data-inizio").value,
        data_fine:   document.getElementById("filtro-data-fine").value,
        descrizione: document.getElementById("filtro-descrizione").value
    })
}

function resetFiltri() {
    document.getElementById("filtro-categoria").value = ""
    document.getElementById("filtro-data-inizio").value = ""
    document.getElementById("filtro-data-fine").value = ""
    document.getElementById("filtro-descrizione").value = ""
    caricaSpese()
}

async function aggiungiSpesa() {
    const importo = document.getElementById("spesa-importo").value
    const categoria = document.getElementById("spesa-categoria").value
    const data = document.getElementById("spesa-data").value
    const descrizione = document.getElementById("spesa-descrizione").value

    if (!importo || !categoria || !data) {
        alert("Importo, categoria e data sono obbligatori")
        return
    }

    try {
        await fetch(`${API_URL}/api/spese`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ importo: parseFloat(importo), categoria, data, descrizione })
        })

        // Svuota il form
        document.getElementById("spesa-importo").value = ""
        document.getElementById("spesa-categoria").value = ""
        document.getElementById("spesa-data").value = ""
        document.getElementById("spesa-descrizione").value = ""

        // Ricarica lista e dashboard
        caricaSpese()
        caricaDashboard()

    } catch (error) {
        console.error("Errore nell'aggiunta della spesa:", error)
    }
}

async function eliminaSpesa(id) {
    if (!confirm("Sei sicuro di voler eliminare questa spesa?")) return

    try {
        await fetch(`${API_URL}/api/spese/${id}`, { method: "DELETE" })
        caricaSpese()
        caricaDashboard()
    } catch (error) {
        console.error("Errore nell'eliminazione della spesa:", error)
    }
}

async function caricaEntrate() {
    try {
        const response = await fetch(`${API_URL}/api/entrate`)
        const entrate = await response.json()
        const lista = document.getElementById("lista-entrate")

        if (entrate.length === 0) {
            lista.innerHTML = `<p class="empty-state">Nessuna entrata registrata</p>`
            return
        }

        lista.innerHTML = entrate.map(entrata => `
            <li class="list-item">
                <div class="list-item-info">
                    <p class="list-item-nome">${entrata.fonte}</p>
                    <p class="list-item-sub">${entrata.data} ${entrata.descrizione ? "· " + entrata.descrizione : ""}</p>
                </div>
                <span class="list-item-importo positivo">+€${entrata.importo.toFixed(2)}</span>
                <button class="btn-delete" onclick="eliminaEntrata(${entrata.id})">✕</button>
            </li>
        `).join("")

    } catch (error) {
        console.error("Errore nel caricamento delle entrate:", error)
    }
}

async function aggiungiEntrata() {
    const importo = document.getElementById("entrata-importo").value
    const fonte = document.getElementById("entrata-fonte").value
    const data = document.getElementById("entrata-data").value
    const descrizione = document.getElementById("entrata-descrizione").value

    if (!importo || !fonte || !data) {
        alert("Importo, fonte e data sono obbligatori")
        return
    }

    try {
        await fetch(`${API_URL}/api/entrate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ importo: parseFloat(importo), fonte, data, descrizione })
        })

        document.getElementById("entrata-importo").value = ""
        document.getElementById("entrata-fonte").value = ""
        document.getElementById("entrata-data").value = ""
        document.getElementById("entrata-descrizione").value = ""

        caricaEntrate()
        caricaDashboard()

    } catch (error) {
        console.error("Errore nell'aggiunta dell'entrata:", error)
    }
}

async function eliminaEntrata(id) {
    if (!confirm("Sei sicuro di voler eliminare questa entrata?")) return

    try {
        await fetch(`${API_URL}/api/entrate/${id}`, { method: "DELETE" })
        caricaEntrate()
        caricaDashboard()
    } catch (error) {
        console.error("Errore nell'eliminazione dell'entrata:", error)
    }
}


async function caricaUltimiMovimenti() {
    try {
        const response = await fetch(`${API_URL}/api/riepilogo/ultimi-movimenti?limite=10`)
        const movimenti = await response.json()
        const lista = document.getElementById("lista-movimenti")

        if (movimenti.length === 0) {
            lista.innerHTML = `<p class="empty-state">Nessun movimento registrato</p>`
            return
        }

        lista.innerHTML = movimenti.map(m => `
            <li class="list-item">
                <div class="list-item-info">
                    <p class="list-item-nome">${m.descrizione}</p>
                    <p class="list-item-sub">${m.data}</p>
                </div>
                <span class="list-item-importo ${m.tipo_movimento === 'spesa' ? 'negativo' : 'positivo'}">
                    ${m.tipo_movimento === 'spesa' ? '-' : '+'}€${m.importo.toFixed(2)}
                </span>
            </li>
        `).join("")

    } catch (error) {
        console.error("Errore nel caricamento dei movimenti:", error)
    }
}


// Viene eseguito al caricamento della pagina
document.addEventListener("DOMContentLoaded", () => {
    caricaDashboard()
    caricaUltimiMovimenti()
    caricaSpese()
    caricaEntrate()
})