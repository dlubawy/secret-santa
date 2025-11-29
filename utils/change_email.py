import argparse
import os

import firebase_admin
from firebase_admin import auth, credentials

HOME = os.environ.get("HOME")
CREDENTIALS = f"{HOME}/.config/firebase/credentials.json"

# Use a service account
cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred)


def main(current_email, new_email):
    user = auth.get_user_by_email(current_email)
    print(f'User: "{vars(user)}"\n')
    updated_user = auth.update_user(user.uid, email=new_email)
    print(f'Updated user: "{vars(updated_user)}"\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update user's email address.")
    parser.add_argument(
        "current_email",
        help="Current user's email address",
    )
    parser.add_argument(
        "new_email",
        help="New user's email address",
    )
    args = parser.parse_args()
    main(args.current_email, args.new_email)
