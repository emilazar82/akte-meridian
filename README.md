# Akte Meridian

Detektiv-Reisespiel im Browser: Zeugen befragen, Hinweise sammeln, Haftbefehl ausstellen und die Spur um die Welt verfolgen.

- 14 Städte mit je drei gemalten Schauplätzen und drei Zeugen
- Zufällig gewürfelte Fälle: 8 Startstädte mit eigener Beute, 120 Routen, 8 mögliche Täter
- Vertonte Dialoge (Ordner `ton/`), Bilder in `szenen/` und `portraits/`
- Läuft ohne Build-Schritt: `index.html` über einen beliebigen Webserver öffnen, z. B. `python -m http.server`

Bilder und Stimmen wurden mit ElevenLabs erzeugt. `werkzeug/` enthält die Stammdaten (`data.py`) und das Arbeitsskript `build_game.py`, mit dem `index.html` zusammengesetzt wurde. Das Skript ist als Referenz abgelegt und läuft in diesem Repository nicht ohne Anpassung.
