from fastapi import FastAPI

from backend.routes import routes
from backend.db.db import Base, Engine
# Main app
app = FastAPI(debug=True)

# Includes router of every sub-app
app.include_router(routes.router)


# Demo/Home endpoint
@app.get("/")
async def home():
    return {"Hello": "World"}
