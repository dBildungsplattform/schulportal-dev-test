# schulportal-ai-collection

Dieses Repository enthält Hilfsmittel für das Testen und die Qualitätssicherung des Schulportals – darunter manuelle Testfälle, Prompts und GitHub Copilot Skills.

---

## GitHub Copilot Skills

Die Skills befinden sich in `.github/skills/` und werden automatisch von GitHub Copilot erkannt und aktiviert. Sie können im Copilot-Chat durch natürliche Sprache ausgelöst werden.

---

### 1. `analyze-requirement`

**Zweck:** Analysiert eine User Story oder Anforderung auf Vollständigkeit, Eindeutigkeit und Qualität anhand von 10 strukturierten Checks. Das Ergebnis ist ein Bericht mit Status-Icons (✅ / ⚠️ / ❌) und einem abschließenden **READY / NOT READY**-Urteil.

**Verwendung:**
> „Analysiere diese User Story: …"  
> „Prüfe die Anforderung auf Lücken: …"  
> „Ist dieses Ticket ready for development?"

Copilot fragt zunächst nach dem Anforderungstext und optionalem Kontext, bevor die Analyse startet.

---

### 2. `generate-test-cases`

**Zweck:** Leitet manuelle Testfälle aus einer Anforderung oder User Story ab und speichert sie als **CSV-Datei für den Xray-Import** unter `.github/manual_tests/`.

**Verwendung:**
> „Erstelle Testfälle für SPSH-1234."  
> „Leite manuelle Tests aus dieser Anforderung ab: …"

Copilot fragt interaktiv nach:
- **Format**: Multi-Test (ein Testfall pro Szenario) oder Single-Test (alle Schritte in einem Testfall)
- **Anforderung**, **Testtiefe** (Positiv, Negativ, Grenzwert)
- **Metadaten**: Ticket-ID, Testplan, Stichwörter, Autor, Repo, Priorität

---

### 3. `generate-api-test-cases`

**Zweck:** Wie `generate-test-cases`, jedoch speziell für **Backend- und API-Tickets**. Die Tests beschreiben HTTP-Aufrufe (Methode, Endpoint, Request-Body, Statuscodes) und eignen sich für den Test über Swagger (`/docs`) oder REST-Clients wie Postman.

**Verwendung:**
> „Erstelle API-Testfälle für den Endpoint POST /api/v1/users."  
> „Testfälle für dieses Backend-Ticket: …"

Copilot fragt interaktiv nach:
- **Format**: Multi-Test oder Single-Test
- **Endpoint(s)**, **Auth-Typ**, **Testtiefe**
- **Metadaten**: Ticket-ID, Testplan, Stichwörter, Autor, Repo, Priorität

---

## Prompt

### `create-test-coverage`

Datei: `.github/prompts/create-test-coverage.prompt.md`

Prüft die Testabdeckung anhand einer definierten Testgegenstandsliste und schreibt das Ergebnis als Markdown-Tabelle nach `test_coverage/testabdeckung.md`.

> **Hinweis:** Dieser Prompt muss im Repository ausgeführt werden, in dem die automatisierten Tests liegen – nicht in diesem Repo. Nur dort hat Copilot Zugriff auf die Testdateien und den Testgegenstand.

---

## Dokumentation

- [Übersicht der KI-Skills und Agenten](docs/uebersicht-der-ki-elemente.md)
- [Testfallerstellung mit GitHub Copilot](docs/testfall-erstellung-ui-tests.md)

## Hilfsskript

Das Skript `.github/scripts/json_to_csv.py` konvertiert die von den Testfall-Skills erzeugten JSON-Daten in das für Xray geeignete CSV-Format.

---

## Ausgabe

Generierte Testfall-CSVs liegen unter `.github/manual_tests/` und sind direkt in Xray importierbar.
