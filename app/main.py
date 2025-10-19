from fastapi import FastAPI
from app.proxy import proxy_request
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Initialize metrics before startup
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "ChronoServe Gateway running"}

app.add_route("/{path:path}", proxy_request, methods=["GET", "POST", "PUT", "DELETE"])
