import httpx
import time
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from app.telemetry import log_request
from app.rl_agent import RLAgent

agent = RLAgent()

BACKENDS = {
    "service1": ["http://service1:8001"],
}

async def proxy_request(request: Request):
    path = request.path_params["path"]
    service_name = path.split("/")[0]

    if service_name not in BACKENDS:
        return JSONResponse({"detail": "Service not found"}, status_code=404)

    backend = agent.choose_backend(service_name, BACKENDS[service_name])
    url = f"{backend}/{path[len(service_name)+1:]}"
    start = time.perf_counter()

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=request.headers.raw,
                content=await request.body(),
                timeout=5.0
            )
        latency = (time.perf_counter() - start) * 1000
        reward = -latency
        agent.update(service_name, backend, reward)
        await log_request(path, latency)
        return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
    except Exception as e:
        return JSONResponse({"detail": f"Proxy error: {str(e)}"}, status_code=500)
