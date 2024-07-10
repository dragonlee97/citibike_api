import os
from google.cloud import bigquery
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def connect_to_bq():
    client = bigquery.Client(project=os.getenv("PROJECT"))
    try:
        yield client
    finally:
        client.close()


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
