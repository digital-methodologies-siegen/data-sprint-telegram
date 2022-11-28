# Parser für Telegram-Kanäle

## Beschreibung

Für den Daten-Sprint im Dezember 2022 wurde über die Telegram-Benutzeroberfläche Content aus zahlreichen Kanälen und Channels heruntergeladen. Diese Daten stehen über die Veranstalter:innen zur Verfügung. 

Das Script `parsing-channels.py` extrahiert aus den vorliegenden html-Seiten die zentralen Datenpunkte und speichert sie in einer csv-Datei.

Dieses Repo ist ein fork von https://github.com/SFB1472/tdp-telegram-channel-scraper


## Benutzung

Im Terminal mittels `cd` in den Ordner navigieren, in dem der Scraper liegt

Virtuell Environment erzeugen mit:
`python3 -m venv venv`

Virtuel Environment starten mit:
`source venv/bin/activate`

notwendige packages installieren mit:
`pip install -r requirements.txt`

Daten von den Veranstalter:innen in einem Ordner `data` auf gleicher Ebene wie der Ordner `scraping` ablegen und entpacken.

`python parsing-channels.py` ausführen

