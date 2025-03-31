
# 🔐 Secure CLI Authentication Tool (Python + Argon2 + SQLite)

Ein kleines, sicheres CLI-Tool zur Benutzerverwaltung mit Passwort-Hashing nach dem Stand der Technik. Es nutzt:

- 🧂 Salt (automatisch in Argon2 enthalten)
- 🌶️ Pepper (aus `.env`)
- 🛡️ Argon2 (empfohlener Hashing-Algorithmus)
- 🗃️ SQLite zur Datenspeicherung

## 📦 Installation

1. **Projekt klonen**  
   ```bash
   git clone https://github.com/eigenwilLich/secure-cli-auth.git
   cd secure-cli-auth
   ```

2. **Virtuelle Umgebung (optional, empfohlen)**  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate.bat   # Windows
   ```

3. **Abhängigkeiten installieren**  
   ```bash
   pip install -r requirements.txt
   ```

4. **.env-Datei anlegen**  
   Erstelle eine `.env`-Datei mit folgendem Inhalt:

   ```
   PEPPER_SECRET=dein_geheimer_pepper
   ```

---

## 🧪 Verwendung

Benutzer registrieren:

```bash
python main.py register benutzername
```

Einloggen:

```bash
python main.py login benutzername
```

---

## 📁 Projektstruktur

```
secure-auth/
├── auth.py           # Logik für Registrierung & Login
├── main.py           # CLI-Einstiegspunkt
├── users.db          # SQLite-Datenbank (automatisch erzeugt)
├── .env              # Enthält geheimen Pepper
├── requirements.txt  # Abhängigkeiten
└── README.md         # Diese Datei
```

---

## 🔐 Sicherheitshinweise

- Der **Pepper** wird nicht gespeichert und erhöht die Sicherheit massiv.
- Die Passwörter werden mit **Argon2 gehasht**, was sehr sicher gegen Brute-Force ist.
- `argon2-cffi` verwendet sichere Voreinstellungen – du kannst diese bei Bedarf anpassen.

---

## ✅ Noch offen?

- Passwort ändern
- Benutzer löschen
- Export in CSV oder JSON

---

## ⚖️ Lizenz

MIT – frei nutzbar.
