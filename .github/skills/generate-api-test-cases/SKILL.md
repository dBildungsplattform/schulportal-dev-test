---
name: generate-api-test-cases
description: 'Derives manual test cases for backend/API tickets and saves them as a CSV file optimized for Xray import. Tests are described at the HTTP level (endpoint, method, request body, status codes) — not via UI. Use when asked to create, derive, or write test cases for an API, endpoint, or backend ticket that is tested via Swagger or a REST client.'
---

# Generate API Test Cases

Dieser Skill leitet aus einer Backend-Anforderung manuelle API-Testfälle ab und speichert sie direkt als **CSV-Datei für den Xray-Import**. Die Tests beschreiben HTTP-Aufrufe (Methode, Endpoint, Request-Body, Statuscodes) — nicht UI-Interaktionen. Im Chat erscheint kein Markdown und keine Tabelle — einziges Ergebnis ist die gespeicherte CSV-Datei.

## Use When
- Du sollst Testfälle für ein Backend-Ticket, einen REST-Endpoint oder eine API-Anforderung erstellen
- Das Testen erfolgt über Swagger (`/docs`), einen REST-Client (z.B. Postman, curl) oder direkte HTTP-Aufrufe
- Es gibt (noch) kein Frontend für den zu testenden Funktionsbereich

## Do Not Use When
- Es sollen UI-Tests erstellt werden → nutze `generate-test-cases`
- Es sollen Playwright-/automatisierte Tests in TypeScript geschrieben werden (normaler Coding-Workflow)
- Es wird nur eine Erklärung oder Analyse einer Anforderung gewünscht, keine Testfälle
- Es sollen Gherkin-Tests geschrieben werden

---

## Step 0 — Kontext sammeln (einmalig je Aufgabe)

**Schritt 1 — Format per Tool abfragen**

Nutze das `vscode_askQuestions`-Tool und stelle genau diese **eine** Frage:

- **Frage**: "Wie sollen die Testfälle strukturiert werden?"
- **Optionen** (Einzelauswahl, kein Freitext):
  - **Multi-Test** — Jedes Szenario bekommt eine eigene TCID
  - **Single-Test** — Alle Prüfungen in einem einzigen Testfall; jede Prüfung wird ein eigener Testschritt

Warte auf die Antwort, bevor du fortfährst.

**Schritt 2 — API-Details und Metadaten im Chat erfragen**

Stelle dem User im Chat folgende Fragen als formatierte Liste. Warte auf die Antwort, bevor du fortfährst:

1. **Anforderung**: Was soll getestet werden? (User Story, Freitext, Ticket-Inhalt, OpenAPI-Auszug)
2. **Endpoint(s)**: HTTP-Methode und Pfad, z.B. `POST /api/v1/users` — kann auch mehrere sein
3. **Auth-Typ**: Wie wird sich authentifiziert?
   - Bearer Token (JWT)
   - Basic Auth
   - Kein Auth erforderlich
   - Sonstiges (bitte beschreiben)
4. **Testtiefe**: Welche Testarten sollen abgedeckt werden? (Mehrfachauswahl möglich)
   - Positiv-Tests (HTTP 2xx, Happy Path)
   - Negativ-Tests (ungültige Eingaben, fehlende Pflichtfelder, HTTP 4xx)
   - Auth-Szenarien (kein Token, abgelaufener Token, falsche Rolle → HTTP 401/403)
   - Grenzwert-Tests (leere Strings, Maximalwerte, Sonderzeichen)
   - Kombinationen der obigen
5. **Metadaten** für alle Testfälle dieser Aufgabe:
   - **Tests** (Ticket-ID, z.B. `"SPSH-234"`)
   - **Beschreibung** (z.B. `"Test aus Playwright importiert."`)
   - **Testplan** (Ticket-ID des zugehörigen Testplans, z.B. `"SPSH-3163"`)
   - **Stichwörter** (eine oder mehrere, z.B. `"DevTest21"`, `"Beschrieben"` — jedes Stichwort ergibt eine eigene Spalte)
   - **Autor** (z.B. `"silvia.grosche"`)
   - **Repo** (z.B. `"Devtest/Sprint 21"`)
   - **Prio** (`"low"`, `"medium"` oder `"high"`)

> **Fahre erst fort, wenn alle Angaben vorliegen.**

---

## Step 0b — Anforderungstext vorverarbeiten (intern — keine Ausgabe)

Ersetze in der gegebenen Anforderung die folgenden Zeichen, bevor du Testfälle ableitest. Dieser Schritt gilt für den gesamten Anforderungstext inkl. Akzeptanzkriterien und Scope. Gib das Ergebnis **nicht** aus.

| Zeichen | Ersetzung |
|---------|-----------|
| `"`     | `'`       |
| `ä`     | `ae`      |
| `ö`     | `oe`      |
| `ü`     | `ue`      |
| `ß`     | `ss`      |

---

## Step 1 — Testfälle ableiten

Leite aus der Anforderung API-Testfälle ab. Wende je nach gewähltem **Format** eine der beiden folgenden Strategien an:

### Format: Multi-Test (Standard)

- Decke alle vom User gewählten Testarten ab (Positiv, Negativ, Auth, Grenzwerte)
- **Alle Schritte eines Testszenarios gehören in die erste Tabellenzeile.** Folgezeilen mit gleicher TCID beschreiben **sequenzielle, aufbauende Schritte** innerhalb desselben Szenarios — sie enthalten nur die Delta-Aktion.
- Eine **neue TCID** entsteht nur, wenn der Test **von vorne beginnt** (anderer Auth-Kontext, anderer Request-Body-Typ, komplett anderes Szenario).
- **Es wird nur geprüft, was die Anforderung betrifft.** Setup-Schritte (Token holen) sind keine eigenen Prüfschritte.
- **Auth-Negativ-Szenarien** (kein Token, falsche Rolle) sind eigene TCIDs.

### Format: Single-Test

- Es gibt genau **eine TCID** für die gesamte Anforderung.
- Die erste Tabellenzeile enthält den Setup-Schritt und den ersten Prüfschritt.
- Jede weitere zu prüfende Bedingung wird eine eigene Folgezeile mit derselben TCID.
- Setup-Schritte (Token holen) stehen nur in der ersten Zeile und erzeugen kein eigenes Erwartetes Ergebnis.

### API-spezifische Ableitungsregeln

- **Happy Path zuerst**: Beginne mit dem erfolgreichen Aufruf (2xx).
- **Negativ-Tests**: Leite Fehlerfälle direkt aus der Anforderung ab — fehlende Pflichtfelder, ungültige Typen, falsche Werte.
- **Auth-Szenarien** (wenn gewählt): Erstelle eigene TCIDs für:
  - Kein Token → HTTP 401
  - Abgelaufener/ungültiger Token → HTTP 401
  - Token mit falscher Rolle / fehlendem Recht → HTTP 403
- **Grenzwert-Tests**: Leere Strings, `null`, Maximalwerte, Sonderzeichen als Request-Body in Data.

---

## Step 2 — Markdown-Tabelle aufbauen (kein Chat-Output)

> **Dieser Step wird intern ausgeführt — es erscheint keine Ausgabe im Chat.**

**2a — Interne Markdown-Tabelle aufbauen**

Baue die Testfälle als interne Markdown-Tabelle mit exakt diesen Spalten in dieser Reihenfolge auf:

```
TCID | tests | Zusammenfassung | Beschreibung | Aktion | Data | Erwartetes Ergebnis | Testplan | Autor | Stichwort | [Stichwort | ...] | Prio | Repo
```

> Jedes vom User angegebene Stichwort erhält eine eigene Spalte, alle mit der Überschrift **Stichwort**.

Tabellenregeln:

- **TCID**: Fortlaufende Nummer, startet bei `1`. Ein Testfall kann mehrere Zeilen haben — alle Zeilen desselben Tests erhalten dieselbe TCID.
- **Metadaten-Regel**: Die Felder tests, Zusammenfassung, Beschreibung, Testplan, Autor, Stichwörter, Prio und Repo stehen **nur in der ersten Zeile** eines Tests — Folgezeilen dieser Spalten bleiben leer. Das Feld **Data** wird in jeder Zeile ausgefüllt (mindestens `-`).
- **Zusammenfassung**: Format `<tests>: <kurze Testbeschreibung>` (z.B. `SPSH-234: POST /api/v1/users – gueltiger Request`).
- **Aktion**: Alle Schritte des Testszenarios, jeder präfixiert mit `# `. Beginnt mit dem Auth-Setup-Schritt, endet mit dem HTTP-Aufruf. Unter-Schritte werden mit `## ` präfixiert.

  Formatierungskonventionen für API-Aktionen (Schritte innerhalb einer Zelle durch `<br>` getrennt):
  - **HTTP-Methoden** → `*GET*`, `*POST*`, `*PUT*`, `*PATCH*`, `*DELETE*`: z.B. `*POST* _/api/v1/users_ aufrufen`
  - **Endpfade / URL-Segmente** → `_..._`: z.B. `_/api/v1/users/{id}_`
  - **Header-Namen** → `_..._`: z.B. `_Authorization_`-Header setzen
  - **Response-Felder / JSON-Keys** → `_..._`: z.B. Response enthaelt `_id_`
  - **Auth-Setup-Schritt**: `# Bearer Token setzen (Daten)` — der konkrete Token/Account steht in **Data**
  - **Kein-Auth-Szenario**: `# Aufruf ohne _Authorization_-Header`

- **Data**: Testdaten passend zum Aktionsschritt dieser Zeile. Enthält:
  - Bearer Token / Rolle / Account-Beschreibung beim Auth-Setup-Schritt
  - Request-Body (JSON oder Feldliste) beim HTTP-Aufruf-Schritt
  - Query-Parameter / Path-Parameter wenn relevant
  - `-` wenn keine Daten relevant sind
- **Erwartetes Ergebnis**: HTTP-Statuscode + fachliches Prüfergebnis, z.B.:
  - `HTTP 201 – Response enthaelt _id_ der angelegten Ressource`
  - `HTTP 400 – Validierungsfehler: _name_ ist Pflichtfeld`
  - `HTTP 401 – Zugriff verweigert (kein Token)`
  - `HTTP 403 – Zugriff verweigert (fehlende Berechtigung)`

---

## Step 3 — Self-Check auf Markdown-Tabelle (intern — keine Ausgabe)

Prüfe die Markdown-Tabelle aus Step 2a intern und korrigiere Fehler, bevor mit Step 4 fortgefahren wird. Gib diesen Check **nicht** aus:

- Die Spaltenanzahl ist in jeder Tabellenzeile konsistent
- Metadaten (tests, Zusammenfassung, Beschreibung, Testplan, Autor, Stichwörter, Prio, Repo) stehen nur in der ersten Zeile je TCID — Folgezeilen dieser Spalten sind leer
- Das Feld **Data** ist in jeder Zeile ausgefüllt (mindestens `-`)
- Die Zusammenfassung folgt dem Format `<tests>: <kurze Testbeschreibung>`
- TCIDs sind konsistent fortlaufend (1, 2, 3, …)
- Jedes Erwartetes Ergebnis beginnt mit einem HTTP-Statuscode (außer bei reinen Setup-Zeilen ohne Prüfschritt)

---

## Step 4 — Markdown-Datei speichern und Skript ausführen (kein Chat-Output)

> **Dieser Step wird intern ausgeführt — es erscheint keine Ausgabe im Chat.**

**4a — Markdown-Datei speichern**

Speichere die Markdown-Tabelle aus Step 2a mit `create_file` als:

- **Pfad**: `.github/manual_tests/<TICKET-ID>-testfaelle.md`
  - `<TICKET-ID>`: Ticket-ID in Originalschreibweise, z.B. `SPSH-3353`

**4b — Skript aufrufen**

Führe das Konvertierungsskript mit `run_in_terminal` aus:

```
python .github/scripts/md_to_csv.py .github/manual_tests/<TICKET-ID>-testfaelle.md --delete-input
```

- `--delete-input` löscht die Markdown-Zwischendatei nach erfolgreicher Konvertierung automatisch.
- Prüfe den Exit-Code: Bei Fehler (Exit-Code ≠ 0) die Fehlermeldung aus stderr im Chat ausgeben und abbrechen.

---

## Step 5 — Abschluss

**Einzige Ausgabe im Chat** nach erfolgreichem Skript-Lauf:

> CSV gespeichert: `.github/manual_tests/<TICKET-ID>-testfaelle.csv`

---

## When the Skill Cannot Proceed

Stop und informiere den User, wenn:
- Die Anforderung zu vage ist, um konkrete HTTP-Aufrufe abzuleiten — bitte um Endpoint und erwartetes Verhalten
- Kein erwartetes Verhalten (Statuscode / Response-Body) aus der Anforderung erkennbar ist — frage nach dem Akzeptanzkriterium
