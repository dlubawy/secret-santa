import csv
import os
import secrets
from collections import namedtuple

import firebase_admin
from firebase_admin import auth, credentials, firestore

HOME = os.environ.get('HOME')
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

USERS = f'{HOME}/.config/secret-santa/users.csv'

with open(USERS, 'r', encoding='utf-8') as csvfile:
    valid_users = {
        row['email']: row['name']
        for row in csv.DictReader(csvfile)
    }

# Use a service account
cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')

for email, name in valid_users.items():
    try:
        user = auth.get_user_by_email(email)
        print(f'User data existed for: {email}')
    except auth.UserNotFoundError:
        user = auth.create_user(email=email,
                                password=secrets.token_urlsafe(14))
        users_ref.document(user.uid).set(dict(name=name, gifts=[]))
        users_ref.document(
            user.uid).collection('private').document('data').set(
                dict(secret=dict(uid='', never=[], previous='')))
        print(f'Created user data for: {email}')
    except Exception as error:
        # TODO: Add logging of the error
        print(error)
