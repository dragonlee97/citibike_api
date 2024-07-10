import os

from datetime import datetime, timezone
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from google.cloud import bigquery

from schemas import UserIn, UserOut
from utils import connect_to_bq, hash


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, client: bigquery.Client = Depends(connect_to_bq)):
    # hash the password - user.password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = {
        "username": user.username,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    user_row = [new_user]
    errors = client.insert_rows_json(client.dataset(os.getenv("DATASET")).table("users"), user_row)
    if errors == []:
        print("New rows have been added.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")
    return {"username": user.username, "created_at": datetime.now(timezone.utc)}
