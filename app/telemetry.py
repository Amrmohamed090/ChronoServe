from app.db import AsyncSessionLocal
from app.models import Telemetry

async def log_request(path: str, latency: float, region: str = "us-east"):
    async with AsyncSessionLocal() as session:
        record = Telemetry(endpoint=path, latency_ms=latency, region=region)
        session.add(record)
        await session.commit()
