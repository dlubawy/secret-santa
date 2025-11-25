"""Creates valid users based on configuration

Will populate firebase authentication with users definged in XDG_CONFIG_HOME/secret-santa/users.csv.
Users defined in the form: `email,name\nfoo@example.com,DisplayName`
"""

import argparse
import csv
import os
import secrets

import firebase_admin
from firebase_admin import auth, credentials, firestore

HOME = os.environ.get("HOME")
CREDENTIALS = f"{HOME}/.config/firebase/credentials.json"

USERS = f"{HOME}/.config/secret-santa/users.csv"

DEFAULT_VALS = dict(name="", gifts=[], secret={}, uid="", never=[], previous="")


def validate_user_data(users_ref, user, name="NoName", reset=False):
    DEFAULT_VALS.update(name=name)
    send_update = False
    doc_ref = users_ref.document(user.uid)
    doc = doc_ref.get()

    if not doc.exists or reset:
        create_user_data(doc_ref, name)
    else:
        doc = doc.to_dict()

        for key in ("name", "gifts"):
            if key not in doc:
                send_update = True
                doc[key] = DEFAULT_VALS[key]
                print(f"Key not found: '{key}'. Creating key.")

            if key == "name" and doc[key] != name:
                send_update = True
                doc[key] = DEFAULT_VALS[key]
                print(f"Key not found: '{key}'. Creating key.")

        if send_update:
            doc_ref.set(doc)
            send_update = False

    private_ref = doc_ref.collection("private").document("data")
    doc = private_ref.get()

    if not doc.exists or reset:
        create_user_data(private_ref, name)
    else:
        doc = doc.to_dict()

        if "secret" not in doc:
            doc["secret"] = DEFAULT_VALS["secret"]
            print("Key not found: 'secret'. Creating key.")

        for key in ("uid", "never", "previous"):
            if key not in doc["secret"]:
                send_update = True
                doc["secret"][key] = DEFAULT_VALS[key]
                print(f"Key not found: '{key}'. Creating key.")

        if send_update:
            private_ref.set(doc)
            send_update = False

    owned_ref = doc_ref.collection("owned").document("data")
    doc = owned_ref.get()

    if not doc.exists or reset:
        create_user_data(owned_ref, name)


def create_user_data(doc_ref, name=""):
    match doc_ref.parent.id:
        case "private":
            doc_ref.set(dict(secret=dict(uid="", never=[], previous="")))
            print(f"Created new private user data for: '{name}'")
        case "owned":
            doc_ref.set(dict(purchasedGifts={}))
            print(f"Created new owned user data for: '{name}'")
        case _:
            doc_ref.set(dict(name=name, gifts=[]))
            print(f"Initialized new user data for: '{name}'")


def main(prod=False):
    if not prod:
        os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9099"

    with open(USERS, "r", encoding="utf-8") as csvfile:
        valid_users = {row["email"]: row["name"] for row in csv.DictReader(csvfile)}

    # Use a service account
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection("users")

    for email, name in valid_users.items():
        try:
            user = auth.get_user_by_email(email)
            if not user.display_name:
                print(f"Display name missing. Adding: {name}.")
                auth.update_user(user.uid, display_name=name)
            print(f"User found for '{email}'.")
        except auth.UserNotFoundError:
            user = auth.create_user(
                display_name=name, email=email, password=secrets.token_urlsafe(14)
            )
            print(f"User not found for '{email}'. Created new user.")
        except Exception as error:
            # TODO: Add logging of the error
            print(error)
            raise error

        validate_user_data(users_ref, user, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create valid user data according to schema."
    )
    parser.add_argument(
        "--prod",
        help="Flag for production use",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    args = parser.parse_args()
    main(args.prod)
