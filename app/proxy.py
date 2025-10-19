import httpx
import time
from fastapi import Request, Response
from app.telemetry import log_request

TARGETS = {
    "/service1": "http://backend1:8000",
    "/service2": "http://backend2:8000"
}

async def proxy_request(request: Request):
    path = request.url.path
    target = next((v for k, v in TARGETS.items() if path.startswith(k)), None)
    if not target:
        return Response("No matching backend", status_code=404)

    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=f"{target}{path}",
            headers=request.headers.raw,
            content=await request.body()
        )
    latency = (time.perf_counter() - start) * 1000
    await log_request(path, latency)
    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
