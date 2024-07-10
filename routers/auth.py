import os

from fastapi import Depends, FastAPI, HTTPException, status, Body, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from jinja2 import Template

from schemas import Token
from oauth2 import create_access_token
from utils import connect_to_bq, verify

router = APIRouter(tags=["Authentification"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), client: bigquery.Client = Depends(connect_to_bq)):
    with open("sql/credentials.sql") as file:
        sql_template = file.read()
    template = Template(sql_template)
    sql_query = template.render(
        project=os.getenv("PROJECT"), dataset=os.getenv("DATASET"), username=user_credentials.username
    )
    try:
        query_job = client.query(sql_query)
        username, hashed_password = next(query_job.result())
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"user login query failed: {e}")

    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User")

    if not verify(user_credentials.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password")

    access_token = create_access_token(data={"user_id": username})

    return {"access_token": access_token, "token_type": "bearer"}
