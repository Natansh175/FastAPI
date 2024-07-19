from fastapi import FastAPI
from backend.routes import routes
app = FastAPI(debug=True)
app.include_router(routes.router)


@app.get("/")
async def home():
    return {"Hello": "World"}
