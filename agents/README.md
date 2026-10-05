# Struttura agentica — Leggi la Polizza per Me

Il prototipo è stato interamente progettato e sviluppato tramite **agentic coding**
con Claude Code, usando la licenza aziendale già disponibile (nessuna API key
Anthropic separata). Questa cartella documenta gli agenti, le istruzioni, i comandi,
i prompt e il workflow usati durante lo sviluppo e usati a runtime dall'applicazione.

## Struttura

| Cartella | Contenuto |
|---|---|
| [`agenti/`](agenti/) | I due agenti applicativi che compongono il backend: l'agente di analisi documentale e l'agente di Q&A |
| [`prompt/`](prompt/) | I system prompt esatti usati per ciascun agente, estratti da `app/main.py` |
| [`comandi/`](comandi/) | Come l'app invoca il CLI Claude Code via subprocess (nessuna API key) |
| [`workflow/`](workflow/) | Le fasi di sviluppo seguite durante l'hackathon, dalla scelta del tema alla consegna |

## In sintesi

- **Nessuna API key Anthropic**: l'app chiama il CLI `claude` già autenticato con
  l'account Accenture tramite `subprocess`, passando i documenti via stdin per
  evitare i limiti di lunghezza della riga di comando di Windows.
- **Due agenti distinti**, ciascuno con un system prompt dedicato e un compito
  circoscritto (estrazione strutturata vs. conversazione guidata).
- **`--restricted`**: ogni invocazione disabilita gli strumenti agentici di
  modifica file/esecuzione comandi, perché qui serve solo generazione di testo.
