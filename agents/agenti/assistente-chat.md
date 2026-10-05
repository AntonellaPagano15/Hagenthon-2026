# Agente 2 — Assistente Chat

## Ruolo
Risponde a domande specifiche in linguaggio naturale sulla polizza caricata,
con un tono caldo e paziente, adatto a chiunque fatichi a comprendere un testo
complesso — per età avanzata, giovane età, disabilità visive o bassa alfabetizzazione.

## Trigger
Invocato a ogni messaggio inviato nella chat (endpoint `POST /chat` in
[`app/main.py`](../../app/main.py)), incluse le domande poste a voce tramite
il microfono (Web Speech API, lato client).

## Input
- Testo integrale del set informativo (stesso documento già analizzato)
- Cronologia degli ultimi 6 scambi della conversazione
- La nuova domanda dell'utente
- System prompt dedicato: [`../prompt/system-chat.md`](../prompt/system-chat.md)

## Output
Una risposta di massimo 3 frasi, sempre con citazione dell'articolo o della
pagina da cui proviene l'informazione.

## Regole comportamentali chiave
- Se l'informazione non è nel documento, lo dichiara esplicitamente invece di
  inventare una risposta plausibile.
- **Non fornisce mai consigli assicurativi** ("dovresti sottoscrivere...",
  "ti conviene...") — spiega solo cosa dice il documento, come richiesto dal
  tema Accessibilità Digitale ("la persona, non l'audit tecnico").
- Linguaggio semplice, frasi brevi, nessun gergo tecnico non spiegato.
