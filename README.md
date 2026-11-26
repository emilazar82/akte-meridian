# Akte Meridian

Detektiv-Reisespiel im Browser: Zeugen befragen, Hinweise sammeln, Haftbefehl ausstellen und die Spur um die Welt verfolgen.

- 14 Städte mit je drei gemalten Schauplätzen und drei Zeugen
- Zufällig gewürfelte Fälle: 8 Startstädte mit eigener Beute, 120 Routen, 8 mögliche Täter
- Vertonte Dialoge (Ordner `ton/`), Bilder in `szenen/` und `portraits/`
- Läuft ohne Build-Schritt: `index.html` über einen beliebigen Webserver öffnen, z. B. `python -m http.server`

Bilder und Stimmen wurden mit ElevenLabs erzeugt. `werkzeug/` enthält die Stammdaten (`data.py`) und das Arbeitsskript `build_game.py`, mit dem `index.html` zusammengesetzt wurde. Das Skript ist als Referenz abgelegt und läuft in diesem Repository nicht ohne Anpassung.

## Stand November 2026

- **Interaktive Szenen:** In jeder Szene stehen gemalte Figuren (`figuren/`). Der Zeuge muss angetippt werden; Nebenfiguren kosten Zeit und wissen nichts.
- **Fundstücke:** In jeder Stadt liegt an einem der drei Orte ein Fundstück (Bordkarten-Abschnitt oder Wechselquittung) als zusätzlicher Hinweis.
- **Schwierigkeitsstufen:** Leicht, Mittel, Schwer. Schwer hat sieben Städte, kryptische Hinweise (`x_*`-Clips), ahnungslose Zeugen (`n_*`) und keine automatischen Notizen.
- **Werkzeug:** `werkzeug/figdata.py` enthält Positionen der Figuren je Szene, `werkzeug/harddata.py` die Texte der Stufe Schwer.
