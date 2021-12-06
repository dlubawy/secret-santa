import json
import os

import firebase_admin
from firebase_admin import auth, credentials, firestore

HOME = os.environ.get('HOME')
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

USER_CONFIG = f'{HOME}/.config/secret-santa/user_config.json'

with open(USER_CONFIG, 'r', encoding='utf-8') as _file:
    configs = json.loads(_file.read())

cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')


def get_uid(email):
    try:
        return auth.get_user_by_email(email).uid
    except auth.UserNotFoundError:
        print(f'User not found for: \'{email}\'')

        return None
    except Exception as error:
        raise error


def update(doc_ref, config):
    if config.get('previous'):
        config.update(previous=get_uid(config['previous']))

    if config.get('never'):
        config.update(never=[get_uid(email) for email in config['never']])
    doc = doc_ref.get()

    if doc.exists:
        doc = doc.to_dict()
        doc['secret'].update(config)
    else:
        doc = dict(secret=dict(uid='', never=[], previous=''))

    doc_ref.set(doc)


for email, config in configs.items():
    user = get_uid(email)

    if user:
        doc_ref = users_ref.document(user)

        if doc_ref.get().exists:
            update(doc_ref.collection('private').document('data'), config)
            print(f'Updated config for: \'{email}\'')
    else:
        print(f'User not found for: \'{email}\'. Skipping.')
