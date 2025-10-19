from app.db import SessionLocal
from app.models import Telemetry

async def log_request(endpoint: str, latency: float, region: str = "us-east"):
    async with SessionLocal() as session:
        entry = Telemetry(endpoint=endpoint, latency_ms=latency, region=region)
        session.add(entry)
        await session.commit()
