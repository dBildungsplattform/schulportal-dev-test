Bitte prüfe die Testabdeckung im folgenden Fall:
Die zu testenden Fälle stehen in test_coverage\testgegenstand.md,
die Tests findest du im Ordner tests.

Lies dazu den Inhalt der relevanten Testdateien – nicht nur deren Namen.
Prüfe, ob der Testgegenstand als eigenständiger describe/test-Block vorkommt
oder nur implizit als Schritt in einem anderen Test abgedeckt wird.

Verwende folgende Status:
- ✅ Vollständig abgedeckt: direkt und vollständig getestet, alle Nutzergruppen berücksichtigt
- ⚠️ Teilweise abgedeckt: implizit, nur ein Teil der Nutzergruppen, oder nur als Nebeneffekt eines anderen Tests
- ❌ Nicht abgedeckt: kein Test vorhanden

Erstelle eine Markdown-Tabelle mit den Spalten:
Nr. | Testgegenstand | Nutzergruppe(n) | Status | Testdatei(en) | Anmerkungen

In der Spalte "Anmerkungen" begründe kurz, warum du den Status so bewertet hast,
besonders bei ⚠️ und ❌.

Schreibe das Ergebnis in test_coverage\testabdeckung.md.
Ergänze am Ende eine Übersicht mit: Anzahl gesamt, ✅, ⚠️, ❌.