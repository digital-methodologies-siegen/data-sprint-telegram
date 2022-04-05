# Scraper für Telegram-Kanäle

## Beschreibung

Dieser Scraper holt auf Basis eines Links alle Beiträge aus einem öffentlichen Telegram-Kanal. 

Es können mehrere Kanäle gescrapt werden. Welche das sein sollen, ist in der channels.csv hinterlegt.

## Benutzung

Im Terminal mittels `cd` in den Ordner navigieren, in dem der Scraper liegt

Virtuell Environment erzeugen mit:
`python3 -m venv venv`

Virtuel Environment starten mit:
`source venv/bin/activate`

notwendige packages installieren mit:
`pip install -r requirements.txt`

`python scraper-channels.py` ausführen

Daten werden direkt in den Ordner `../data/raw/` gespeichert. 
Gewährleisten, dass der Ordner existiert!

## Bekannte Schwachstellen

- Scraper sollten nur Daten ziehen, nicht gleich noch Daten parsen (extrahieren). Besser wäre dieser Scraper speichert html-Seiten, die von einem neuen Script ausgelesen werden

- Es kommt vor, dass der Scraper bricht, weil der Server zu lange braucht zu anworten. Das zu manuell zu fixen ist einfach:
-- Auf der Console wird ausgegeben, bei welchen Link der Fehler auftrat
-- Diesen Link kopieren
-- channels.csv duplizieren und neuen Namen geben
-- channels.csv öffnen, Kanäle, die schon fertig gescrapt sind löschen, Link aus der Konsole bei der Person einfügen, bei der der Fehler auftrat
-- Script erneut starten