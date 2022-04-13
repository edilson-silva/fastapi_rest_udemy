from fastapi import FastAPI

__version__ = "0.1.0"

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Welcome to API!"}
