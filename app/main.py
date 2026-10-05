import json
import os
import subprocess
import tempfile

import pdfplumber
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Polizza in Chiaro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLAUDE_CLI = os.path.expandvars(r"%USERPROFILE%\.local\bin\claude.exe")

# In-memory store (single-user prototype)
document_store: dict = {"text": "", "filename": ""}

ANALYZE_SYSTEM = """Sei un esperto di polizze assicurative italiane (salute, vita, auto, casa, infortuni e altri rami).
Analizza il set informativo fornito e restituisci un JSON con questa struttura esatta:
{
  "prodotto": "nome del prodotto assicurativo",
  "coperture": [{"voce": "...", "dettaglio": "...", "riferimento": "art. X / pag. Y"}],
  "esclusioni": [{"voce": "...", "dettaglio": "...", "riferimento": "art. X / pag. Y", "impatto": "alto|medio|basso"}],
  "sinistro": [{"passo": 1, "azione": "...", "dettaglio": "..."}],
  "costi": {"premio": "...", "franchigia": "...", "massimale": "...", "pagamento": "...", "riferimento": "pag. X"}
}
Usa frasi brevi (max 15 parole per voce). Rispondi SOLO con JSON valido, senza blocchi markdown, nessun testo aggiuntivo."""

CHAT_SYSTEM = """Sei un assistente che aiuta chiunque fatichi a comprendere un testo complesso — per età
avanzata, giovane età, disabilità visive o bassa alfabetizzazione — a capire la propria polizza assicurativa.

REGOLE:
- Rispondi in massimo 3 frasi semplici e chiare
- Cita sempre l'articolo o la pagina dove trovi l'informazione (es. "Come indicato all'art. 4, pag. 12...")
- Se l'informazione non è nel documento, dillo esplicitamente
- Non dare consigli assicurativi o di acquisto
- Usa un tono caldo e paziente"""


def call_claude(system_prompt: str, stdin_message: str) -> str:
    """Invoke the Claude Code CLI non-interactively, piping the (possibly large) content via stdin."""
    result = subprocess.run(
        [CLAUDE_CLI, "-p", "--restricted", "--output-format", "text",
         "--system-prompt", system_prompt],
        input=stdin_message,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Errore nell'esecuzione del CLI Claude Code")
    return result.stdout.strip()


def strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else ""
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(BASE_DIR, "static", "index.html"), encoding="utf-8") as f:
        return f.read()


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text_parts = []
        with pdfplumber.open(tmp_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        full_text = "\n".join(text_parts)
        document_store["text"] = full_text
        document_store["filename"] = file.filename

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "pages": page_count,
            "chars": len(full_text),
        })
    finally:
        os.unlink(tmp_path)


@app.post("/analyze")
async def analyze():
    if not document_store["text"]:
        return JSONResponse({"error": "Nessun documento caricato"}, status_code=400)

    text = document_store["text"][:80000]
    stdin_message = f"Analizza questo set informativo:\n\n{text}"

    try:
        raw = call_claude(ANALYZE_SYSTEM, stdin_message)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    cleaned = strip_code_fence(raw)

    try:
        result = json.loads(cleaned)
        return JSONResponse(result)
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Errore nel parsing della risposta AI", "raw": raw[:500]},
            status_code=500,
        )


@app.post("/chat")
async def chat(payload: dict):
    if not document_store["text"]:
        return JSONResponse({"error": "Nessun documento caricato"}, status_code=400)

    user_message = payload.get("message", "").strip()
    history = payload.get("history", [])

    if not user_message:
        return JSONResponse({"error": "Messaggio vuoto"}, status_code=400)

    text = document_store["text"][:80000]

    history_text = "".join(
        f"{'Utente' if h['role'] == 'user' else 'Assistente'}: {h['content']}\n"
        for h in history[-6:]
    )

    stdin_message = f"""SET INFORMATIVO:
{text}

CONVERSAZIONE PRECEDENTE:
{history_text or "(nessuna)"}

NUOVA DOMANDA DELL'UTENTE:
{user_message}"""

    try:
        response_text = call_claude(CHAT_SYSTEM, stdin_message)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    return JSONResponse({"response": response_text})


app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
