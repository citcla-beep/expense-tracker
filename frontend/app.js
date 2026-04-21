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

// Carica le categorie e popola tutti i dropdown
async function caricaCategorie() {
    try {
        const response = await fetch(`${API_URL}/api/categorie`)
        const categorie = await response.json()

        // Popola il select nel form aggiungi spesa
        const selectSpesa = document.getElementById("spesa-categoria")
        selectSpesa.innerHTML = `<option value="">Seleziona categoria</option>`
        categorie.forEach(c => {
            selectSpesa.innerHTML += `<option value="${c.nome}">${c.nome}</option>`
        })

        // Popola il select nel form cerca spese
        const selectFiltro = document.getElementById("filtro-categoria")
        selectFiltro.innerHTML = `<option value="">Tutte le categorie</option>`
        categorie.forEach(c => {
            selectFiltro.innerHTML += `<option value="${c.nome}">${c.nome}</option>`
        })

        // Popola la lista nella sezione categorie
        const lista = document.getElementById("lista-categorie")
        if (categorie.length === 0) {
            lista.innerHTML = `<p class="empty-state">Nessuna categoria</p>`
            return
        }
        lista.innerHTML = categorie.map(c => `
            <li class="list-item">
                <div class="list-item-info">
                    <p class="list-item-nome">${c.nome}</p>
                </div>
                <button class="btn-delete" onclick="eliminaCategoria(${c.id})">✕</button>
            </li>
        `).join("")

    } catch (error) {
        console.error("Errore nel caricamento delle categorie:", error)
    }
}

async function aggiungiCategoria() {
    const nome = document.getElementById("categoria-nome").value.trim()

    if (!nome) {
        alert("Inserisci un nome per la categoria")
        return
    }

    try {
        const response = await fetch(`${API_URL}/api/categorie`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome })
        })

        if (!response.ok) {
            const errore = await response.json()
            alert(errore.detail)
            return
        }

        document.getElementById("categoria-nome").value = ""
        caricaCategorie()

    } catch (error) {
        console.error("Errore nell'aggiunta della categoria:", error)
    }
}

async function eliminaCategoria(id) {
    if (!confirm("Sei sicuro di voler eliminare questa categoria?")) return

    try {
        await fetch(`${API_URL}/api/categorie/${id}`, { method: "DELETE" })
        caricaCategorie()
    } catch (error) {
        console.error("Errore nell'eliminazione della categoria:", error)
    }
}

async function caricaFonti() {
    try {
        const response = await fetch(`${API_URL}/api/fonti`)
        const fonti = await response.json()

        // Popola il select nel form aggiungi entrata
        const selectEntrata = document.getElementById("entrata-fonte")
        selectEntrata.innerHTML = `<option value="">Seleziona fonte</option>`
        fonti.forEach(f => {
            selectEntrata.innerHTML += `<option value="${f.nome}">${f.nome}</option>`
        })

        // Popola la lista nella sezione fonti
        const lista = document.getElementById("lista-fonti")
        if (fonti.length === 0) {
            lista.innerHTML = `<p class="empty-state">Nessuna fonte</p>`
            return
        }
        lista.innerHTML = fonti.map(f => `
            <li class="list-item">
                <div class="list-item-info">
                    <p class="list-item-nome">${f.nome}</p>
                </div>
                <button class="btn-delete" onclick="eliminaFonte(${f.id})">✕</button>
            </li>
        `).join("")

    } catch (error) {
        console.error("Errore nel caricamento delle fonti:", error)
    }
}

async function aggiungiFonte() {
    const nome = document.getElementById("fonte-nome").value.trim()

    if (!nome) {
        alert("Inserisci un nome per la fonte")
        return
    }

    try {
        const response = await fetch(`${API_URL}/api/fonti`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome })
        })

        if (!response.ok) {
            const errore = await response.json()
            alert(errore.detail)
            return
        }

        document.getElementById("fonte-nome").value = ""
        caricaFonti()

    } catch (error) {
        console.error("Errore nell'aggiunta della fonte:", error)
    }
}

async function eliminaFonte(id) {
    if (!confirm("Sei sicuro di voler eliminare questa fonte?")) return

    try {
        await fetch(`${API_URL}/api/fonti/${id}`, { method: "DELETE" })
        caricaFonti()
    } catch (error) {
        console.error("Errore nell'eliminazione della fonte:", error)
    }
}




// Viene eseguito al caricamento della pagina
document.addEventListener("DOMContentLoaded", () => {
    caricaDashboard()
    caricaUltimiMovimenti()
    caricaSpese()
    caricaEntrate()
    caricaCategorie()
    caricaFonti()
})