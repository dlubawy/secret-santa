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

DEFAULT_VALS = dict(name='',
                    gifts=[],
                    secret={},
                    uid='',
                    never=[],
                    previous='')


def validate_user_data(user, name='NoName', reset=False):
    DEFAULT_VALS.update(name=name)
    send_update = False
    doc_ref = users_ref.document(user.uid)
    doc = doc_ref.get()

    if not doc.exists or reset:
        create_user_data(doc_ref, name)
    else:
        doc = doc.to_dict()

        for key in ('name', 'gifts'):
            if key not in doc:
                send_update = True
                doc[key] = DEFAULT_VALS[key]
                print(f'Key not found: \'{key}\'. Creating key.')

            if key == 'name' and doc[key] != name:
                send_update = True
                doc[key] = DEFAULT_VALS[key]
                print(f'Key not found: \'{key}\'. Creating key.')

        if send_update:
            doc_ref.set(doc)
            send_update = False

    doc_ref = doc_ref.collection('private').document('data')
    doc = doc_ref.get()

    if not doc.exists or reset:
        create_user_data(doc_ref, name)
    else:
        doc = doc.to_dict()

        if 'secret' not in doc:
            doc['secret'] = DEFAULT_VALS['secret']
            print(f'Key not found: \'secret\'. Creating key.')

        for key in ('uid', 'never', 'previous'):
            if key not in doc['secret']:
                send_update = True
                doc['secret'][key] = DEFAULT_VALS[key]
                print(f'Key not found: \'{key}\'. Creating key.')

        if send_update:
            doc_ref.set(doc)
            send_update = False


def create_user_data(doc_ref, name=''):
    if doc_ref.id == 'data':
        doc_ref.set(dict(secret=dict(uid='', never=[], previous='')))
    else:
        doc_ref.set(dict(name=name, gifts=[]))
    print(f'Created new user data for: \'{user.email}\'')


for email, name in valid_users.items():
    try:
        user = auth.get_user_by_email(email)
        print(f'User found for \'{email}\'.')
    except auth.UserNotFoundError:
        user = auth.create_user(email=email,
                                password=secrets.token_urlsafe(14))
        print(f'User not found for \'{email}\'. Created new user.')
    except Exception as error:
        # TODO: Add logging of the error
        print(error)
        raise error

    validate_user_data(user, name)
