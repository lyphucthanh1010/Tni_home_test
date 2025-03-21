from fastapi import FastAPI
from routers import upload, history

app = FastAPI()

app.include_router(upload.router, prefix="/api")
app.include_router(history.router, prefix="/api")
