from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field, SecretStr


class StationRequest(BaseModel):
    request_id: str
    station: str
    start_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")

    # Python 3.10 + pydantic v2
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "request_id": "r1",
                    "station": "A very nice Item",
                    "start_date": "2017-01-01",
                    "end_date": "2017-12-31",
                }
            ]
        }
    }


class StationReponse(BaseModel):
    request_id: str
    departures: int
    arrivals: int


class UserDemographicsResponse(BaseModel):
    young_male: int
    young_female: int
    middle_aged_male: int
    middle_aged_female: int
    elder_male: int
    elder_female: int


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
