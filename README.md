# Polizza in Chiaro

**Hagenthon 2026 · Tema 01 — Accessibilità Digitale**

Un agente che legge il set informativo di qualsiasi polizza al posto
dell'utente, risponde a domande specifiche citando sempre la fonte (articolo
o pagina), e genera un riepilogo di una pagina — la **Carta della Polizza** —
da tenere a portata di mano.

## Il problema

Chiunque fatichi a comprendere un testo complesso — per età avanzata, giovane
età, disabilità visive o bassa alfabetizzazione — riceve il set informativo
di una polizza (40-100+ pagine di linguaggio legale) e non riesce a capire
cosa è davvero coperto, quali sono le esclusioni più importanti, né cosa fare
in caso di sinistro. Rinuncia a leggere, oppure firma senza aver capito.

## La soluzione

1. **Carica il PDF** del set informativo
2. L'agente lo **analizza** ed estrae coperture, esclusioni (con livello di
   impatto), procedura in caso di sinistro e costi — ogni voce con
   riferimento ad articolo/pagina
3. L'utente fa **domande libere**, anche **a voce**, e riceve risposte brevi
   con citazione della fonte
4. Un click genera la **Carta della Polizza**, un riepilogo stampabile

## Struttura del repository

```
/
├── app/           → il prototipo funzionante (FastAPI + frontend)
├── agents/        → la struttura agentica: agenti, prompt, comandi, workflow
├── presentation/  → la presentazione della soluzione (brand Accenture)
└── README.md
```

## Avviare il prototipo

Richiede Python 3.12+ e il [CLI Claude Code](https://claude.ai/install.ps1)
già autenticato (`claude /login`) — nessuna API key necessaria.

```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

Apri `http://127.0.0.1:8080`.

## Perché nessuna API key

L'app invoca il CLI Claude Code via subprocess, sfruttando la licenza
Accenture già attiva sulla macchina. Dettagli completi in
[`agents/comandi/cli-invocation.md`](agents/comandi/cli-invocation.md).

## Autonomia & limiti

Lo strumento **spiega** il documento così come è scritto: non fornisce
consulenza assicurativa, non sostituisce un intermediario abilitato, e lo
dichiara esplicitamente ogni volta che un'informazione non è presente nel
documento caricato.
