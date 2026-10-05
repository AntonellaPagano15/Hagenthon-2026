# Invocazione del CLI Claude Code

L'app non usa l'SDK Anthropic né una API key separata: chiama direttamente il
binario `claude` già autenticato con la licenza Accenture, via `subprocess`
Python (`call_claude()` in [`app/main.py`](../../app/main.py)).

## Comando effettivo

```python
subprocess.run(
    [CLAUDE_CLI, "-p", "--restricted", "--output-format", "text",
     "--system-prompt", system_prompt],
    input=stdin_message,   # il documento + la domanda, passati via stdin
    capture_output=True,
    text=True,
    timeout=180,
)
```

Equivalente da riga di comando:

```bash
claude -p --restricted --output-format text --system-prompt "<prompt>" <<< "<messaggio>"
```

## Perché stdin e non argomento posizionale

Windows limita la lunghezza della riga di comando passata a `CreateProcess`
(~32.000 caratteri circa). Il testo di un set informativo può superare gli
80.000 caratteri: passarlo come argomento CLI avrebbe troncato o rotto la
chiamata. Il flag `--input-format text` (default di `-p`) legge il contenuto
da stdin, che non ha questo limite — per questo il documento viaggia sempre
come `input=` del subprocess, mai come argomento.

## Perché `--restricted`

Disabilita gli strumenti agentici che normalmente il CLI mette a disposizione
(Bash, modifica file, WebFetch): qui serve solo generazione di testo a partire
da un prompt, senza che il modello possa eseguire comandi o toccare il
filesystem del server.

## Autenticazione

Nessuna chiave in codice o in `.env`. Il CLI usa la sessione già autenticata
con `claude /login` (OAuth, account Accenture) sulla macchina che esegue il
backend — la stessa identità con cui si usa Claude Code per sviluppare.
