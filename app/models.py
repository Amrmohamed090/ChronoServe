from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.db import Base
from datetime import datetime

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    latency_ms = Column(Float)
    region = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
