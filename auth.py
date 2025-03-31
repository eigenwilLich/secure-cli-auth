import os
import sqlite3
import json
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from getpass import getpass

# .env laden
load_dotenv()

# Datenbankname festlegen (anpassbar)
DB_NAME = "users.db"
ph = PasswordHasher()


def get_secret_pepper():
    """Lädt den geheimen Pepper aus der Umgebung."""
    return os.getenv("PEPPER_SECRET", "default_pepper").encode()


def init_db():
    """Erstellt die SQLite-Datenbank und gibt eine Verbindung zurück."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def register_user(conn, username):
    """
    Registriert einen neuen Benutzer mit Passwort + Pepper + Argon2.
    Gibt True bei Erfolg, False wenn der Benutzer existiert.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("❌ Benutzer existiert bereits.")
        return False

    password = getpass("🔐 Passwort eingeben: ")
    pepper = get_secret_pepper()
    combined = password.encode() + pepper

    hashed = ph.hash(combined)
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    print("✅ Registrierung erfolgreich.")
    return True


def login_user(conn, username):
    """
    Überprüft Benutzername und Passwort.
    Gibt True bei Erfolg, False bei Fehler.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if not result:
        print("❌ Benutzer nicht gefunden.")
        return False

    password = getpass("🔐 Passwort eingeben: ")
    pepper = get_secret_pepper()
    combined = password.encode() + pepper

    try:
        ph.verify(result[0], combined)
        print("✅ Login erfolgreich.")
        return True
    except VerifyMismatchError:
        print("❌ Falsches Passwort.")
        return False
    except Exception as e:
        print(f"⚠️ Fehler: {e}")
        return False
    

def change_password(conn, username):
    """
    Ändert das Passwort eines bestehenden Benutzers.
    Gibt True bei Erfolg, False bei Fehler.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if not result:
        print("❌ Benutzer nicht gefunden.")
        return False

    # Aktuelles Passwort prüfen
    current_pw = getpass("🔐 Aktuelles Passwort: ")
    pepper = get_secret_pepper()
    combined_current = current_pw.encode() + pepper

    try:
        ph.verify(result[0], combined_current)
    except VerifyMismatchError:
        print("❌ Aktuelles Passwort ist falsch.")
        return False

    # Neues Passwort abfragen (zweifache Eingabe)
    new_pw_1 = getpass("🔑 Neues Passwort: ")
    new_pw_2 = getpass("🔁 Passwort bestätigen: ")

    if new_pw_1 != new_pw_2:
        print("❌ Passwörter stimmen nicht überein.")
        return False

    combined_new = new_pw_1.encode() + pepper
    new_hash = ph.hash(combined_new)

    cursor.execute("UPDATE users SET hashed_password = ? WHERE username = ?", (new_hash, username))
    conn.commit()
    print("✅ Passwort erfolgreich geändert.")
    return True


def delete_user(conn, username):
    """
    Löscht einen Benutzer nach Passwortbestätigung.
    Gibt True bei Erfolg, False bei Fehler.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if not result:
        print("❌ Benutzer nicht gefunden.")
        return False

    # Passwortabfrage zur Bestätigung
    password = getpass("🔐 Passwort zur Bestätigung: ")
    pepper = get_secret_pepper()
    combined = password.encode() + pepper

    try:
        ph.verify(result[0], combined)
    except VerifyMismatchError:
        print("❌ Passwort falsch.")
        return False
    except Exception as e:
        print(f"⚠️ Fehler: {e}")
        return False

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print("🗑️ Benutzer erfolgreich gelöscht.")
    return True


def list_users(conn):
    """
    Gibt eine Liste aller Benutzernamen aus der Datenbank aus.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username ASC")
    users = cursor.fetchall()

    if not users:
        print("📭 Keine Benutzer vorhanden.")
        return

    print("📋 Benutzerliste:")
    for user in users:
        print(f" - {user[0]}")


def export_users_to_json(conn, filename="users.json"):
    """
    Exportiert alle Benutzernamen aus der Datenbank in eine JSON-Datei.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username ASC")
    users = cursor.fetchall()

    if not users:
        print("📭 Keine Benutzer vorhanden. Export abgebrochen.")
        return False

    usernames = [user[0] for user in users]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(usernames, f, indent=2, ensure_ascii=False)

    print(f"📁 {len(usernames)} Benutzer erfolgreich in '{filename}' exportiert.")
    return True
