import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Body, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jinja2 import Template
from schemas import TokenData
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from utils import connect_to_bq

SECRET_KEY = "3ac6467f6ef28e66781efee17956d2cca86c2a11396c494af046778c7855760d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), client: bigquery.Client = Depends(connect_to_bq)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)

    with open("sql/credentials.sql") as file:
        sql_template = file.read()
    template = Template(sql_template)
    sql_query = template.render(project=os.getenv("PROJECT"), dataset=os.getenv("DATASET"), username=token.username)
    try:
        query_job = client.query(sql_query)
        user, _ = next(query_job.result())
    except BadRequest as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"user token verification failed: {e}"
        )
    return user
