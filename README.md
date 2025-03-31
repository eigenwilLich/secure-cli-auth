
# 🔐 Secure CLI Authentication Tool (Python + Argon2 + SQLite)

Ein sicheres, modular aufgebautes CLI-Tool zur Benutzerverwaltung. 

## ✅ Unterstützte Funktionen

- 🧂 Salt: automatisch in Argon2 enthalten
- 🌶️ Pepper: aus `.env` geladen
- 🔐 Passwort-Hashing mit Argon2
- 🗃️ SQLite als einfache Datenbanklösung
- 👤 Benutzerregistrierung
- 🔓 Login mit Passwortprüfung
- 🔄 Passwort ändern (mit Bestätigung)
- 🗑️ Benutzer löschen (nach Passwortprüfung)
- 📃 Benutzer auflisten
- 📤 Benutzer als JSON-Datei exportieren

---

## Installation

1. **Projekt klonen**
   ```bash
   git clone https://github.com/eigenwilLich/secure-cli-auth.git
   cd secure-cli-auth
   ```

2. **Virtuelle Umgebung erstellen (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate.bat   # Windows
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **.env-Datei anlegen**
   ```ini
   PEPPER_SECRET=dein_geheimer_pepper
   ```

---

## Nutzung

```bash
python cli.py register benutzername      # Benutzer registrieren
python cli.py login benutzername         # Login durchführen
python cli.py change benutzername        # Passwort ändern
python cli.py delete benutzername        # Benutzer löschen
python cli.py list                       # Alle Benutzer auflisten
python cli.py export                     # Benutzer nach users.json exportieren
```

---

## 📁 Projektstruktur

```
secure-cli-auth/
├── auth.py           # Alle Funktionen zur Benutzerverwaltung
├── cli.py            # CLI-Einstiegspunkt (Argumentparser)
├── users.db          # SQLite-Datenbank (automatisch erstellt)
├── .env              # Enthält geheimes PEPPER_SECRET
├── .gitignore        # Ignoriert sensible/temporäre Dateien
├── requirements.txt  # Abhängigkeiten
└── README.md         # Diese Datei
```

---

## 🔐 Sicherheitshinweise

- Der **Pepper** sollte geheim bleiben – verwende `.env`, niemals fest im Code!
- **Argon2** ist aktuell einer der sichersten Algorithmen für Passwort-Hashing.
- Alle Passwortoperationen erfolgen sicher (kein Klartext-Speichern oder -Vergleich).

---

## 🧠 und in Zukunft?

- [ ] Admin-Funktion mit Login
- [ ] Import aus JSON
- [ ] Web-Frontend (Flask, Django)
- [ ] Logging mit `logging`-Modul

---

## ⚖️ Lizenz

MIT – frei nutzbar, veränderbar und erweiterbar.
