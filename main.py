from fastapi import FastAPI
import uvicorn

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
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, log_level="info",
                reload=True)
