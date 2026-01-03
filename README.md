# DokScan

Automated Document Processing Service for scanned files.

## Einfache Anleitung (auch für Anfänger)

### Was ist DokScan?
DokScan ist ein Programm, das automatisch gescannte Dokumente (wie Rechnungen oder Briefe) verarbeitet. Es liest den Text aus, erkennt, um was es geht, und legt alles ordentlich ab. Du kannst es auf deinem Computer oder einem Raspberry Pi laufen lassen.

### Schritt 1: Vorbereitung
Du brauchst Python und Tesseract auf deinem Gerät.

#### Für Windows:
1. Gehe zu [python.org](https://www.python.org/downloads/) und lade Python 3.11 oder neuer herunter.
2. Installiere es (kreuze "Add Python to PATH" an).
3. Lade Tesseract von [hier](https://github.com/UB-Mannheim/tesseract/wiki) herunter und installiere es.

#### Für Raspberry Pi (mit Raspberry Pi OS):
1. Öffne das Terminal und gib ein: `sudo apt update && sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-deu`

### Schritt 2: DokScan herunterladen und installieren
1. Gehe zu [GitHub](https://github.com/IsaSKuehl/DokScan) und lade das Projekt als ZIP herunter (grüner "Code"-Button > "Download ZIP").
2. Entpacke die ZIP-Datei in einen Ordner, z.B. "DokScan".
3. Öffne ein Terminal (Windows: Suche nach "cmd" oder "PowerShell"; Raspberry Pi: Terminal-App).
4. Gehe in den DokScan-Ordner: `cd Pfad/zum/DokScan`
6. Installiere die nötigen Programme: 
   - Windows: 
     - Zuerst: `python -m pip install Pillow`
     - Dann: `python -m pip install -r requirements.txt`
   - Raspberry Pi: `python3 -m pip install -r requirements.txt`

### Schritt 3: Konfiguration
1. Kopiere die Datei `.env.example` zu `.env` (rechtsklick > Kopieren, dann Einfügen und umbenennen).
2. Öffne `.env` mit einem Texteditor (z.B. Notepad).
3. Hol dir einen OpenAI API-Key:
   - Gehe zu [openai.com](https://platform.openai.com/api-keys).
   - Melde dich an und erstelle einen neuen Key.
   - Kopiere ihn und setze ihn in `.env` bei `OPENAI_API_KEY=dein_key_hier`
4. Öffne `config/config.yaml` mit einem Texteditor.
5. Ändere die Pfade:
   - `hotfolder_path`: Ordner, wo du gescannte Dateien reinlegst, z.B. "C:/Scans" oder "/home/pi/scans"
   - `processed_path`: Ordner für verarbeitete Dateien, z.B. "C:/Processed" oder "/home/pi/processed"
   - Andere Pfade ähnlich anpassen.
6. Wenn du Microsoft (Kalender und OneDrive) willst:
   - Setze `enable_microsoft_integration: true`
   - Folge der Microsoft Graph Setup-Anleitung unten.

### Schritt 4: Starten
- Im Terminal: 
  - Windows: `python src/main.py`
  - Raspberry Pi: `python3 src/main.py`
- Es läuft jetzt und wartet auf neue Dateien im Hotfolder.

### Schritt 5: Testen
1. Lege eine gescannte PDF-Datei (z.B. eine Rechnung) in den Hotfolder.
2. Warte ein bisschen – DokScan verarbeitet sie automatisch.
3. Schau in den Processed-Ordner: Dort sollte eine neue PDF mit Report sein.

### Wenn etwas nicht funktioniert
- Schau ins Terminal: Dort stehen Fehlermeldungen.
- Stelle sicher, dass alle Pfade existieren (erstelle die Ordner, wenn nötig).
- Bei Problemen: Überprüfe, ob Python und Tesseract richtig installiert sind.

## Features

- Automatic processing of incoming scan files (PDF, JPG, PNG, TIFF)
- Text extraction with OCR fallback
- Document classification and data extraction using OpenAI LLM
- PDF report generation with summary and key data
- Intelligent file renaming
- Calendar event creation for due payments
- Upload to OneDrive with structured folders
- Tax relevance marking

## Setup (Advanced)

### Prerequisites

- Python 3.11+
- Tesseract OCR

#### Install Tesseract

**Windows:**
Download from https://github.com/UB-Mannheim/tesseract/wiki

**Raspberry Pi OS:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-deu
```

### Installation

1. Clone the repo
2. Install dependencies: 
   - Windows: 
     - First: `python -m pip install Pillow`
     - Then: `python -m pip install -r requirements.txt`
   - Linux/Raspberry Pi: `python3 -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your keys
4. Edit `config/config.yaml` with your paths

### Microsoft Graph Setup (optional)

If `enable_microsoft_integration: true` in config.yaml:

1. Register an app in Azure AD
2. Add permissions: Calendars.ReadWrite, Files.ReadWrite
3. Set Client ID and Tenant ID in .env

### Running

As service:

**Windows:** Use NSSM to create a service pointing to `python src/main.py`

**Raspberry Pi:** Create systemd service

```bash
sudo nano /etc/systemd/system/dokscan.service
```

Content:
```
[Unit]
Description=DokScan Service

[Service]
ExecStart=/usr/bin/python3 /path/to/src/main.py
WorkingDirectory=/path/to/project
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable dokscan
sudo systemctl start dokscan
```

## Configuration

See `config/config.yaml` for options.

## JSON Schema

The LLM output follows the schema in `llm_output_schema.json`.

## Testing

Run `pytest` in the tests directory.

## Demo

Place a sample PDF in the hotfolder and observe processing.