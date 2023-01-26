from threading import Thread
from fastapi import FastAPI
from dotenv import dotenv_values
from routers import k11
import uvicorn


app = FastAPI()
app.include_router(k11.router)


@app.get("/")
async def root():
    return {"message": "Hello FastAPI "}



