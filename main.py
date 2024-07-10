from fastapi import Depends, FastAPI, HTTPException, status, Body
from routers import auth, users, insights


api = FastAPI()


api.include_router(insights.router)
api.include_router(users.router)
api.include_router(auth.router)


@api.get("/")
def root():
    return {"message": "Hello World !"}
