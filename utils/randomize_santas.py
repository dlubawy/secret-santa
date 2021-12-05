import os
import random
from collections import deque
from itertools import tee

import firebase_admin
from firebase_admin import auth, credentials, firestore

HOME = os.environ.get('HOME')
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

# Use a service account
cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')

docs = list(users_ref.list_documents())
available = deque(docs.copy())
random.shuffle(available)

for doc in docs:
    data = doc.collection('private').document('data').get().to_dict()
    never = set(data['secret']['never'])
    secret = available.popleft()

    while doc == secret or doc in never:
        available.append(secret)
        secret = available.popleft()

        if len(available) <= 1:
            break

    data.update(secret=dict(uid=secret.id, previous=data['secret']['uid']))
    doc.collection('private').document('data').set(data)
