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
    link = auth.generate_password_reset_link(email)
    print(f'Password reset link: "{link}"')


if __name__ == '__main__':
    main(sys.argv[1])
