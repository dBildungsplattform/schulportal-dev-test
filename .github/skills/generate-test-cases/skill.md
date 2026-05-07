---
name: generate-test-cases
description: 'Derives manual test cases from a requirement and saves them directly as a CSV file optimized for Xray import. Use when asked to create, derive, or write manual test cases from a requirement, user story, or ticket.'
---

# Generate Manual Test Cases

Dieser Skill leitet aus einer Anforderung manuelle Testfälle ab und speichert sie direkt als **CSV-Datei für den Xray-Import**. Im Chat erscheint kein Markdown und keine Tabelle — einziges Ergebnis ist die gespeicherte CSV-Datei.

## Use When
- Du sollst manuelle Testfälle aus einer Anforderung, User Story oder einem Ticket erstellen
- Du wirst gebeten, Testfälle für einen bestimmten Funktionsbereich abzuleiten

## Do Not Use When
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

**Schritt 2 — Restliche Angaben im Chat erfragen**

Stelle dem User im Chat folgende Fragen als formatierte Liste. Warte auf die Antwort, bevor du fortfährst:

1. **Anforderung**: Was soll getestet werden? (User Story, Freitext, Ticket-Inhalt)
2. **Testtiefe**: Welche Testarten sollen abgedeckt werden? (Mehrfachauswahl möglich)
   - Positiv-Tests (Happy Path)
   - Negativ-Tests (Fehlerfälle, ungültige Eingaben)
   - Grenzwert-Tests
   - Kombinationen der obigen
3. **Metadaten** für alle Testfälle dieser Aufgabe:
   - **Tests** (Ticket-ID, z.B. `"SPSH-234"`)
   - **Beschreibung** (z.B. `"Test aus Playwright importiert."`)
   - **Testplan** (Ticket-ID des zugehörigen Testplans, z.B. `"SPSH-3163"`)
   - **Stichwörter** (eine oder mehrere, z.B. `"Automatisiert"`, `"Beschrieben"` — jedes Stichwort ergibt eine eigene Spalte in der Tabelle)
   - **Autor** (z.B. `"silvia.grosche"`)
   - **Repo** (z.B. `"Automatisierung/Navigieren"`)
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

Leite aus der Anforderung Testfälle ab. Wende je nach gewähltem **Format** eine der beiden folgenden Strategien an:

### Format: Multi-Test (Standard)

- Decke alle vom User gewählten Testarten ab (Positiv, Negativ, Grenzwerte, Kombinationen)
- **Alle Schritte eines Testszenarios (Vorbedingungen + fachliche Aktion) gehören in die erste Tabellenzeile.** Folgezeilen mit gleicher TCID beschreiben **sequenzielle, aufbauende Schritte** — sie enthalten nur die **Delta-Aktion** (was sich gegenüber dem Vorgänger ändert), keinen wiederholten Setup.
- Eine **neue TCID** entsteht nur, wenn der Test **von vorne beginnt** (neuer Kontext, komplett neues Setup). Sequenziell aufbauende Varianten (z.B. schrittweise veränderte Testdaten im gleichen Ablauf) bleiben in einer TCID.
- **Es wird nur geprüft, was die Anforderung betrifft.** Vorbereitende Schritte (Anmelden, Navigation) sind keine eigenen Prüfschritte und erzeugen kein eigenes Erwartetes Ergebnis.

### Format: Single-Test

- Es gibt genau **eine TCID** für die gesamte Anforderung.
- Die erste Tabellenzeile enthält Vorbedingungen und den ersten Prüfschritt.
- **Jede weitere zu prüfende Bedingung aus der Anforderung** wird eine eigene Folgezeile mit derselben TCID — die Aktion beschreibt die Delta-Aktion bzw. den nächsten Prüfschritt, das Erwartete Ergebnis das zugehörige Prüfergebnis.
- Vorbereitende Schritte (Anmelden, Navigation) stehen nur in der ersten Zeile und erzeugen kein eigenes Erwartetes Ergebnis.
- **Es wird nur geprüft, was die Anforderung betrifft.**

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
- **Zusammenfassung**: Format `<tests>: <kurze Testbeschreibung>` (z.B. `SPSH-234: Login mit gueltigen Daten`).
- **Aktion**: Alle Schritte des Testszenarios, jeder präfixiert mit `# `. Beginnt mit Vorbereitungsschritten (Anmelden, Navigation), endet mit der fachlich relevanten Aktion. Beim Anmelde-Schritt steht **ausschließlich die Rollenbezeichnung** (z.B. `# Als Schuladmin anmelden`). **Niemals** Systemrechte oder Account-Details in die Aktion — diese gehören in **Data**. Unter-Schritte werden mit `## ` präfixiert.
  Formatierungskonventionen (innerhalb der Aktion-Zelle, Schritte durch `<br>` getrennt):
  - **Buttons** → `*...*`: z.B. `*Schliessen* klicken`
  - **UI-Elemente, Eigennamen, Seitentitel** → `_..._`: z.B. `_Klassenverwaltung_ oeffnen`
  - **Gesuchte Texte, Meldungen** → `_..._`: z.B. `_Erfolgsmeldung: Der Vorgang wurde ausgefuehrt._`
- **Data**: Testdaten passend zum Aktionsschritt dieser Zeile. Wenn keine Daten relevant sind: `-`.
- **Erwartetes Ergebnis**: Das fachlich relevante Prüfergebnis der Zeile, **ohne** `# ` Präfix. Pro Tabellenzeile genau ein Erwartetes Ergebnis — das des letzten anforderungsrelevanten Schritts.

---

## Step 3 — Self-Check auf Markdown-Tabelle (intern — keine Ausgabe)

Prüfe die Markdown-Tabelle aus Step 2a intern und korrigiere Fehler, bevor mit Step 4 fortgefahren wird. Gib diesen Check **nicht** aus:

- Die Spaltenanzahl ist in jeder Tabellenzeile konsistent
- Metadaten (tests, Zusammenfassung, Beschreibung, Testplan, Autor, Stichwörter, Prio, Repo) stehen nur in der ersten Zeile je TCID — Folgezeilen dieser Spalten sind leer
- Das Feld **Data** ist in jeder Zeile ausgefüllt (mindestens `-`)
- Die Zusammenfassung folgt dem Format `<tests>: <kurze Testbeschreibung>`
- TCIDs sind konsistent fortlaufend (1, 2, 3, …)

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
- Die Anforderung zu vage ist, um konkrete Testschritte abzuleiten — bitte um Präzisierung
- Kein erwartetes Verhalten aus der Anforderung erkennbar ist — frage nach dem Akzeptanzkriterium