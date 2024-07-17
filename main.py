from fastapi import FastAPI, HTTPException
from backend.routes import routes
app = FastAPI()
app.include_router(routes.router)


@app.get("/")
async def home():
    return {"Hello": "World"}
