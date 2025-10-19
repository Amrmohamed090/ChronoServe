from fastapi import FastAPI, Request
from app.proxy import proxy_request
from app.db import Base, engine
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.middleware("http")
async def proxy_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return PlainTextResponse(generate_latest())
    return await proxy_request(request)
