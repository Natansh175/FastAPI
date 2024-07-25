from fastapi import FastAPI

from backend.routes import routes

# Main app
app = FastAPI(debug=True, title="Basic E-Commerce API", version="1.0.0",
              summary="A basic E-Commerce API with applied security for "
                      "managing products and learning how to make "
                      "REST APIs."
              )

# Includes router of every sub-app
app.include_router(routes.router)


# Demo/Home endpoint
@app.get("/")
async def home():
    return {"Hello": "World"}
