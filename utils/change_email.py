import os
import sys

import firebase_admin
from firebase_admin import auth, credentials

HOME = os.environ.get('HOME')
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

# Use a service account
cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred)


def main(email):
    user = auth.get_user_by_email(email)
    print(f'User: "{vars(user)}"\n')
    updated_user = auth.update_user(user.uid, email=email)
    print(f'Updated user: "{vars(updated_user)}"\n')


if __name__ == '__main__':
    main(sys.argv[1])
