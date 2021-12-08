import configparser
import csv
import os
from datetime import datetime, timedelta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

HOME = os.environ.get('HOME')
USERS = f'{HOME}/.config/secret-santa/users.csv'
EMAIL_CONFIG = f'{HOME}/.config/sendgrid/config.ini'

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
        to_emails=emails,
        subject='🎁 New Secret Santa! 🎁',
        html_content=
        f'<p>Secret Santa has been updated! <a href="secret-santa.andrewlubawy.com">Login</a> '\
        f'to view your new assignment and please make sure your own wish list is up to date. '\
        f'<strong>Lists should be finalized by December {day}!</strong></p>'
    )
    #pylint:enable=line-too-long

    return message


def send(message):
    try:
        send_grid = SendGridAPIClient(API_KEY)
        response = send_grid.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as error:
        print(error)


msg = new_santa_msg(email_list)
send(msg)
