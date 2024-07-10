import os

from fastapi import Depends, FastAPI, HTTPException, status, Body, APIRouter
from schemas import StationRequest, StationReponse, UserDemographicsResponse
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from jinja2 import Template
from utils import connect_to_bq
from oauth2 import get_current_user

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/user_demographics", response_model=UserDemographicsResponse)
def user_demographics(client: bigquery.Client = Depends(connect_to_bq), current_user: int = Depends(get_current_user)):
    with open("sql/user_demographics.sql") as file:
        sql_template = file.read()
    template = Template(sql_template)
    sql_query = template.render(project=os.getenv("PROJECT"), dataset=os.getenv("DATASET"))
    try:
        query_job = client.query(sql_query)
        result = next(query_job.result())
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"sql query failed: {e}")
    return {
        "young_male": result[0],
        "young_female": result[1],
        "middle_aged_male": result[2],
        "middle_aged_female": result[3],
        "elder_male": result[4],
        "elder_female": result[5],
    }


@router.post("/station_traffic", response_model=StationReponse)
def station_traffic(
    station_request: StationRequest = Body(..., embed=True),
    client: bigquery.Client = Depends(connect_to_bq),
    current_user: int = Depends(get_current_user),
):
    with open("sql/station_traffic.sql") as file:
        sql_template = file.read()
    template = Template(sql_template)
    sql_query = template.render(
        station_request=station_request, project=os.getenv("PROJECT"), dataset=os.getenv("DATASET")
    )
    try:
        query_job = client.query(sql_query)
        departures, arrivals = next(query_job.result())
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"sql query failed: {e}")
    return {"request_id": station_request.request_id, "departures": departures, "arrivals": arrivals}
