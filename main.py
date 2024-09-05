from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, HttpUrl
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Подключение папки с шаблонами
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

class URLData(BaseModel):
    url: HttpUrl

@app.get("/")
async def main():
    return FileResponse("templates/index.html")

@app.post("/getURL")
async def handle_post(data: URLData):
    # Обработка полученных данных
    return JSONResponse(content={"message": "URL получен", "url": str(data.url)}, status_code=status.HTTP_201_CREATED)

