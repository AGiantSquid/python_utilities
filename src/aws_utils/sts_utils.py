from typing import Callable
from datetime import datetime, timedelta


def get_credential_creator(role_arn: str, role_session_name: str, boto3) -> Callable:
    '''Returns a function that returns valid credentials.'''

    get_creds = lambda: get_credentials(role_arn, role_session_name, boto3)

    def wrapped():
        credentials_gen = credentials_generator(
            get_credentials=get_creds,
            cur_time=datetime.now(),
            expires_at=datetime.now() - timedelta(minutes=1),
            credentials=None,
        )
        return next(credentials_gen)

    return wrapped


def get_credentials(role_arn: str, role_session_name: str, boto3):
    '''Returns fresh credentials for role.'''
    sts_client = boto3.client('sts')

    assumed_role_object=sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )

    credentials = assumed_role_object['Credentials']

    return credentials


def credentials_generator(
        get_credentials: Callable,
        cur_time: datetime,
        expires_at: datetime,
        credentials=None,
    ):
    '''Generator expression that returns existing credentials if unexpired.

    If existing credentials are expired, create a new one when called.'''

    if cur_time > expires_at:
        credentials = get_credentials()
        expiration = cur_time + timedelta(minutes=55)
    else:
        credentials = credentials
        expiration = expires_at

    yield credentials
    yield from credentials_generator(
        get_credentials,
        datetime.now(),
        expiration,
        credentials,
    )
