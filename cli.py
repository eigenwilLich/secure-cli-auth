import argparse
from auth import (
    init_db, register_user, login_user,
    change_password, delete_user, list_users,
    export_users_to_json
)


def main():
    parser = argparse.ArgumentParser(description="🛡️ Sichere Auth mit SQLite + Argon2 + Pepper")
    parser.add_argument("action", choices=["register", "login", "change", "delete", "list", "export"], help="Aktion auswählen")
    parser.add_argument("username", nargs="?", help="Benutzername (optional bei 'list')")

    args = parser.parse_args()
    conn = init_db()

    success = False
    if args.action == "register":
        if not args.username:
            print("❗ Benutzername erforderlich für Registrierung.")
        else:
            success = register_user(conn, args.username)
    elif args.action == "login":
        if not args.username:
            print("❗ Benutzername erforderlich für Login.")
        else:
            success = login_user(conn, args.username)
    elif args.action == "change":
        if not args.username:
            print("❗ Benutzername erforderlich für Passwortänderung.")
        else:
            success = change_password(conn, args.username)
    elif args.action == "delete":
        if not args.username:
            print("❗ Benutzername erforderlich zum Löschen.")
        else:
            success = delete_user(conn, args.username)
    elif args.action == "list":
        list_users(conn)
        success = True
    elif args.action == "export":
        success = export_users_to_json(conn)


    conn.close()
    if not success:
        exit(1)
