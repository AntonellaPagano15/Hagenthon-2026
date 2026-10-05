# Agente 1 — Analizzatore Polizza

## Ruolo
Trasforma un set informativo assicurativo (PDF di 40-100+ pagine, linguaggio
legale/tecnico) in una struttura dati semplice e navigabile, pensata per una
persona senza competenze assicurative.

## Trigger
Invocato una sola volta per documento, quando l'utente clicca **Analizza
Documento** (endpoint `POST /analyze` in [`app/main.py`](../../app/main.py)).

## Input
- Testo integrale del PDF estratto con `pdfplumber` (troncato a 80.000 caratteri)
- System prompt dedicato: [`../prompt/system-analyze.md`](../prompt/system-analyze.md)

## Output
JSON strutturato in 4 sezioni, ciascuna con riferimento ad articolo/pagina:

```json
{
  "prodotto": "nome del prodotto assicurativo",
  "coperture": [{"voce": "...", "dettaglio": "...", "riferimento": "art. X / pag. Y"}],
  "esclusioni": [{"voce": "...", "dettaglio": "...", "riferimento": "...", "impatto": "alto|medio|basso"}],
  "sinistro": [{"passo": 1, "azione": "...", "dettaglio": "..."}],
  "costi": {"premio": "...", "franchigia": "...", "massimale": "...", "pagamento": "..."}
}
```

## Perché un impatto per esclusione
Il campo `impatto` (alto/medio/basso) permette all'interfaccia di evidenziare
in rosso acceso le esclusioni più pericolose — quelle che un utente non esperto
rischia di scoprire solo al momento del sinistro, quando è troppo tardi.

## Vincolo di design
L'agente **non simula** o **non deduce** coperture non scritte nel documento:
riporta solo ciò che è esplicitamente presente nel testo, con citazione della
fonte — per rispettare il vincolo "semplificare senza tradire" del tema
Accessibilità Digitale.
