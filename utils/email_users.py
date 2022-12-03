import argparse
import configparser
import csv
import os
from datetime import datetime, timedelta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

HOME = os.environ.get('HOME')
USERS = f'{HOME}/.config/secret-santa/users.csv'
EMAIL_CONFIG = f'{HOME}/.config/sendgrid/config.ini'
CREDENTIALS = f'{HOME}/.config/firebase/credentials.json'

config = configparser.ConfigParser()
config.read(EMAIL_CONFIG)
API_KEY = config['secret-santa']['API_KEY']

with open(USERS, 'r', encoding='utf-8') as csvfile:
    email_list = [row['email'] for row in csv.DictReader(csvfile)]


def new_santa_msg(emails):
    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) *
                                                (n % 10 < 4) * n % 10::4])
    year = datetime.utcnow().year
    christmas = datetime.strptime(f'{year}-12-25', '%Y-%m-%d')
    day = ordinal((christmas - timedelta(weeks=2)).day)
    #pylint:disable=line-too-long
    message = Mail(
        from_email='secret-santa@andrewlubawy.com',
        bcc_emails=emails,
        subject='🎁 New Secret Santa! 🎁',
        html_content=
        f'<p>Secret Santa has been updated! <a href="secret-santa.andrewlubawy.com">Login</a> '\
        f'to view your new assignment and please make sure your own wish list is up to date. '\
        f'<strong>Lists should be finalized by December {day}!</strong></p>'
    )
    #pylint:enable=line-too-long

    return message


def get_missing_msgs(emails):
    import firebase_admin
    from firebase_admin import auth, credentials, firestore

    emails = [emails] if isinstance(emails, str) else emails

    # Use a service account
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection('users')

    missing = set()

    for email in emails:
        user = auth.get_user_by_email(email)
        doc = users_ref.document(user.uid).get()

        if doc.exists:
            gifts = doc.to_dict()['gifts']

            if not gifts:
                missing.add(email)

    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) *
                                                (n % 10 < 4) * n % 10::4])
    year = datetime.utcnow().year
    christmas = datetime.strptime(f'{year}-12-25', '%Y-%m-%d')
    day = ordinal((christmas - timedelta(weeks=2)).day)
    #pylint:disable=line-too-long
    messages = []

    for email in missing:
        messages.append(Mail(
            from_email='secret-santa@andrewlubawy.com',
            bcc_emails=email,
            subject='You don\'t have any gifts!',
            html_content=
            f'<p>You are running out of time! '\
            f'<strong>Lists should be finalized by December {day}!</strong></p> '\
            f'Please <a href="secret-santa.andrewlubawy.com">login</a> '\
            f'to update your wish list now.'\
        ))
    #pylint:enable=line-too-long

    return messages


def send(message):
    try:
        send_grid = SendGridAPIClient(API_KEY)
        response = send_grid.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as error:
        print(error)


def main(args):
    if args.new_santa:
        msg = new_santa_msg(email_list)
        send(msg)

    if args.missing_gifts:
        msgs = get_missing_msgs(email_list)

        for msg in msgs:
            send(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--new_santa", action="store_true")
    parser.add_argument("--missing_gifts", action="store_true")
    args = parser.parse_args()
    main(args)
