# Workflow di sviluppo

Fasi effettivamente seguite durante l'hackathon, tutte guidate tramite
conversazione con Claude Code (agentic coding).

## 1. Scelta del tema e ideazione
- Confronto tra Tema 01 (Accessibilità Digitale) e Tema 03 (Educazione
  Digitale Inclusiva) rispetto a vincoli di tempo (3 ore) e dimostrabilità.
- Scelto il **Tema 01**: demo prima/dopo più netta, confini del problema più
  precisi (una persona, un servizio, un blocco preciso).
- Idea derivata dagli esempi del brief ma non coincidente: non "semplificare
  un testo" né "guidare un form", bensì **interpretare un intero set
  informativo assicurativo** e renderlo navigabile con domande libere.
- Adattamento al dominio assicurativo salute/vita su richiesta del team.

## 2. Scaffolding
- Generato con Claude Code: backend FastAPI (`app/main.py`) con 3 endpoint
  (`/upload`, `/analyze`, `/chat`) e frontend HTML/JS a pagina singola
  (`app/static/index.html`) con Tailwind via CDN.
- Layout a due colonne: visualizzatore PDF a sinistra, analisi a tab + chat
  a destra.

## 3. Autenticazione senza API key
- Prima ipotesi (API key Anthropic in `.env`) scartata su richiesta: il team
  vuole usare la licenza Claude Code aziendale già disponibile.
- Individuato ed eseguito l'installer ufficiale (`irm https://claude.ai/install.ps1 | iex`).
- Login OAuth del CLI (`claude` → `/login`) con l'account Accenture.
- Backend riscritto per invocare il CLI via `subprocess` invece dell'SDK
  Anthropic (dettagli in [`../comandi/cli-invocation.md`](../comandi/cli-invocation.md)).

## 4. Documento reale e test end-to-end
- Recuperato un set informativo vita reale di UnipolSai (U20019 Vita Premium,
  44 pagine) per validare il prototipo su un documento vero, non sintetico.
- Verificata l'intera pipeline: upload → estrazione testo (`pdfplumber`) →
  analisi strutturata → chat con citazione della fonte → generazione della
  "Carta della Polizza" stampabile.
- Individuato e corretto un bug di layout: su viewport stretti i bottoni e le
  tab andavano a capo, schiacciando l'area contenuti a quasi 0px di altezza.

## 5. Rifiniture di accessibilità
- Messaggi di attesa rotanti durante l'analisi (60-90s con il CLI) per
  rassicurare l'utente invece di uno spinner muto.
- Input vocale nella chat tramite Web Speech API del browser (`it-IT`),
  invio automatico a fine dettatura — pensato per un utente che fatica a
  digitare, coerente con il target del tema.

## 6. Consegna
- Repository riorganizzato in `app/`, `agents/`, `presentation/` come da
  modalità di consegna.
- Installati Git e GitHub CLI, autenticazione via browser (device flow),
  push su repository pubblico.
