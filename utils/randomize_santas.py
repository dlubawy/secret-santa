"""Randomizes secret santa users for the next year.

This will randomly generate new secret santa pairings among users. It reads from the firestore DB
and will:
  1. Remove gifts marked purchased from the previous year (from the user they were purchased for)
  2. Unlock all wishlist locks
  3. Randomly generate pairs using the user's never list and previous pairing to prevent certain matches
"""

import argparse
import os
import random
from collections import deque

import firebase_admin
from firebase_admin import credentials, firestore

HOME = os.environ.get("HOME")
CREDENTIALS = f"{HOME}/.config/firebase/credentials.json"


def remove_purchased_gifts(purchased_gifts, doc):
    new_gifts = list(
        filter(lambda x: x not in purchased_gifts, doc.get(["gifts"]).get("gifts"))
    )
    doc.update({"gifts": new_gifts})


def main(prod=False):
    if not prod:
        os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9099"

    # Use a service account
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection("users")

    docs = list(users_ref.list_documents())
    docs_map = {doc.id: doc for doc in docs}
    available = deque(docs.copy())
    random.shuffle(available)

    for idx, doc in enumerate(docs):
        doc.update({"isLocked": False})
        owned_data = doc.collection("owned").document("data").get().to_dict()
        data = doc.collection("private").document("data").get().to_dict()
        if owned_data["purchasedGifts"]:
            remove_purchased_gifts(
                owned_data["purchasedGifts"], docs_map[data["secret"]["uid"]]
            )
            owned_data.update(purchasedGifts={})
        never = set(data["secret"]["never"])
        never.add(data["secret"]["previous"])
        never.add(data["secret"]["uid"])
        secret = available.popleft()

        seen = set([secret.id])

        while secret.id == doc.id or secret.id in never:
            available.append(secret)
            secret = available.popleft()

            if secret.id in seen:
                raise RuntimeError(f"Unable to make a match for '{doc.id}'!")
            seen.add(secret.id)

        data.update(
            secret={
                "uid": secret.id,
                "previous": data["secret"]["uid"],
                "never": data["secret"]["never"],
            }
        )
        doc.collection("private").document("data").set(data)


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
