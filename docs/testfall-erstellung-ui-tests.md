# Testfallerstellung mit GitHub Copilot

Diese Anleitung beschreibt, wie mit dem Copilot-Skill `generate-test-cases` aus einer Anforderung manuelle Testfälle erstellt und als CSV für den Import in Xray gespeichert werden.

---

## Überblick: Der Workflow

```
Anforderung (Ticket / User Story)
        ↓
[1] generate-test-cases  →  CSV-Datei unter .github/manual_tests/
        ↓
Xray-Import
```

Der Workflow besteht aus **einem Schritt**. Copilot fragt alle nötigen Informationen ab und speichert das Ergebnis direkt als importierbare CSV-Datei — es erscheint keine Markdown-Tabelle im Chat.

---

## Vorbereitung: Was du vor dem ersten Schritt brauchst

Bevor du Copilot anweist, Testfälle zu erstellen, solltest du folgende Informationen parat haben:

| Information    | Beispiel                                   | Bedeutung                                              |
|----------------|--------------------------------------------|--------------------------------------------------------|
| **Anforderung**| Ticket-Text, Akzeptanzkriterien, Freitext  | Was soll getestet werden?                              |
| **Testtiefe**  | Positiv, Negativ, Grenzwerte               | Welche Arten von Tests sollen abgedeckt werden?       |
| **tests**      | `SPSH-234`                                 | Jira-Ticket-ID, der die Testfälle zugeordnet werden   |
| **Beschreibung**| `"Test aus Playwright importiert."`       | Kurze Beschreibung für alle Testfälle dieser Aufgabe  |
| **Testplan**   | `SPSH-3163`                                | Ticket-ID des zugehörigen Testplans in Jira           |
| **Stichwörter**| `Automatisiert`, `Beschrieben`             | Xray-Labels; jedes Stichwort wird eine eigene Spalte  |
| **Autor**      | `silvia.grosche`                           | Jira-Benutzername                                     |
| **Repo**       | `Automatisierung/Navigieren`               | Pfad im Repo, dem die Testfälle thematisch zugeordnet sind |
| **Prio**       | `low` / `medium` / `high`                 | Priorität der Testfälle                               |

---

## Testfälle erstellen (`generate-test-cases`)

### Wie du Copilot aktivierst

Schreibe in den Copilot-Chat z.B.:

> „Erstelle Testfälle für folgende Anforderung: [Ticket-Text einfügen]"

oder

> „Leite manuelle Testfälle aus dieser User Story ab: [...]"

### Was Copilot als erstes fragt

Copilot öffnet zunächst einen **Dialog** und fragt nach dem gewünschten Format:

| Format | Beschreibung |
|--------|--------------|
| **Multi-Test** | Jedes Szenario bekommt eine eigene TCID |
| **Single-Test** | Alle Prüfungen in einem einzigen Testfall; jede Prüfung wird ein eigener Testschritt |

Danach fragt Copilot im Chat nach:

1. **Anforderung** — Was soll getestet werden? (User Story, Freitext, Ticket-Inhalt)
2. **Testtiefe** — Positiv-Tests, Negativ-Tests, Grenzwert-Tests oder Kombinationen
3. **Metadaten** — Ticket-ID, Testplan, Stichwörter, Autor, Repo, Priorität

### Was Copilot ausgibt

Nach der Eingabe aller Informationen arbeitet Copilot intern und gibt **ausschließlich** folgendes im Chat aus:

> `CSV gespeichert: .github/manual_tests/<TICKET-ID>-testfaelle.csv`

Es erscheint keine Markdown-Tabelle im Chat. Die fertige CSV-Datei liegt direkt unter:

```
.github/manual_tests/<TICKET-ID>-testfaelle.csv
```

Beispiel: `.github/manual_tests/SPSH-234-testfaelle.csv`

**Wichtige Formatdetails der CSV:**
- Trennzeichen: `;`
- Zeilenumbrüche innerhalb von Zellen werden als echte Zeilenumbrüche kodiert (wie Alt+Enter in Excel)
- Anführungszeichen in Zellen werden als `""` escaped
- Jedes Stichwort hat eine eigene Spalte (auch wenn der Spaltenname mehrfach vorkommt — das ist gewollt für Xray)

---

## Häufige Fragen

**Welche Testarten gibt es?**
- **Positiv-Test (Happy Path):** Korrekte Eingaben → System verhält sich wie erwartet.
- **Negativ-Test:** Falsche oder fehlende Eingaben → System zeigt korrekte Fehlermeldung.
- **Grenzwert-Test:** Extremwerte (leer, zu lang, Sonderzeichen) → System verhält sich stabil.

**Wo liegt der Unterschied zwischen `tests` und `Testplan`?**
`tests` ist die ID des Tickets, dem die einzelnen Testfälle zugeordnet werden (z.B. das Feature-Ticket). `Testplan` ist die ID des übergeordneten Testplan-Tickets in Jira/Xray.

---
