from pyexpat.errors import messages

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/home")
async def home():
    return {"message: It's home's page"}