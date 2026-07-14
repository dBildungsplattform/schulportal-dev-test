# Übersicht der KI-Skills und Agenten

> Stand: 19.06.2026

## Skills

Das Repository enthält **drei Skills**, die unter `.github/skills/` abgelegt sind.

### 1. analyze-requirement
**Pfad:** `.github/skills/analyze-requirement/SKILL.md`

Analysiert eine User Story oder Anforderung auf Vollständigkeit, Klarheit und Umsetzungsreife. Dabei werden 10 strukturierte Qualitäts-Checks durchlaufen — von Zielklarheit und Mehrdeutigkeit über betroffene Prozesse, Daten, Akzeptanzkriterien, Nicht-Funktionalien, fehlende Informationen, Testbarkeit, Annahmen & Risiken bis hin zur abschließenden Go/No-Go-Bewertung. Das Ergebnis ist ein strukturierter Bericht mit Status-Icons (✅ / ⚠️ / ❌) pro Check und einem finalen **READY / NOT READY**-Urteil.

**Wann einsetzen:**
- Eine User Story oder ein Ticket vor der Entwicklung geprüft werden soll
- Lücken, Unklarheiten oder Risiken in einer Spezifikation identifiziert werden müssen

---

### 2. generate-test-cases
**Pfad:** `.github/skills/generate-test-cases/skill.md`

Leitet aus einer Anforderung **manuelle UI-Testfälle** ab und speichert sie als CSV-Datei für den Xray-Import. Der Skill deckt Positiv-Tests, Negativ-Tests, Grenzwert-Tests und Kombinationen ab. Die Testfälle werden entweder im **Multi-Test-Format** (jedes Szenario erhält eine eigene TCID) oder im **Single-Test-Format** (alle Prüfungen in einer TCID) erstellt. Im Chat erscheint kein Markdown — einziges Ergebnis ist die gespeicherte CSV unter `.github/manual_tests/`.

**Wann einsetzen:**
- Manuel Testfälle für UI-Funktionalität aus einer User Story abgeleitet werden sollen
- Testfälle für den Import in Xray benötigt werden

---

### 3. generate-api-test-cases
**Pfad:** `.github/skills/generate-api-test-cases/SKILL.md`

Leitet aus einer Backend- oder API-Anforderung **manuelle API-Testfälle** ab und speichert sie als CSV-Datei für den Xray-Import. Die Tests beschreiben HTTP-Aufrufe (Endpoint, Methode, Request-Body, Statuscodes) — nicht UI-Interaktionen. Es werden Positiv-Tests, Negativ-Tests, Auth-Szenarien (401/403) und Grenzwert-Tests unterstützt. Der Output folgt demselben Format wie `generate-test-cases` (Multi-Test oder Single-Test) und wird unter `.github/manual_tests/` als CSV abgelegt.

**Wann einsetzen:**
- Testfälle für REST-Endpoints, API-Tickets oder Backend-Funktionalität erstellt werden sollen
- Tests über Swagger, Postman oder curl durchgeführt werden (kein Frontend vorhanden)

---

## Agenten

Das Repository enthält **keine eigenen Custom Agents**.

---

## Prompts

Das Repository enthält derzeit **eine Prompt-Vorlage** unter `.github/prompts/`.

### 1. create-test-coverage.prompt.md
**Pfad:** `.github/prompts/create-test-coverage.prompt.md`

Prompt-Vorlage zur strukturierten Erstellung von Testabdeckungs-Reports. Sie dient als Ausgangspunkt, um aus vorhandenen Testanforderungen nachvollziehbare Coverage-Übersichten abzuleiten.

**Wann einsetzen:**
- Wenn ein Testabdeckungsreport für die automatisierten Tests erstellt werden soll
- Wenn transparent dargestellt werden soll, welche Anforderungen bereits durch automatisierte Tests abgedeckt sind
- Wenn dargestellt werden soll, welche Tests noch nicht automatisiert sind

---

## Sonstige KI-spezifische Dateien

| Datei | Beschreibung |
|-------|-------------|
| `.github/copilot-instructions.md` | Anweisungen für GitHub Copilot (derzeit leer) |
| `.github/scripts/md_to_csv.py` | Hilfs-Skript zum Konvertieren von Markdown-Tabellen in CSV (wird von `generate-test-cases` und `generate-api-test-cases` verwendet) |
