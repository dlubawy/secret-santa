import csv
import json
import os

import firebase_admin
from firebase_admin import auth, credentials, firestore

HOME = os.environ.get('HOME')
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

USERS = f'{HOME}/.config/secret-santa/users.csv'
USER_CONFIG = f'{HOME}/.config/secret-santa/user_config.json'

with open(USERS, 'r', encoding='utf-8') as csvfile:
    valid_users = {
        row['email']: row['name']
        for row in csv.DictReader(csvfile)
    }

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


def main():
    config = {}

    for email in valid_users.keys():
        user = get_uid(email)

        if user:
            doc_ref = users_ref.document(user)

            if doc_ref.get().exists:
                doc = doc_ref.collection('private').document(
                    'data').get().to_dict()
                config[email] = dict(never=[],
                                     previous=auth.get_user(
                                         doc['secret']['previous']).email)

                for uid in doc['secret']['never']:
                    config[email]['never'].append(auth.get_user(uid).email)
        else:
            print(f'User not found for: \'{email}\'. Skipping.')

    print(f'Updating config:\n{config}')
    with open(USER_CONFIG, "w", encoding="utf-8") as _file:
        _file.write(json.dumps(config))


if __name__ == '__main__':
    main()
