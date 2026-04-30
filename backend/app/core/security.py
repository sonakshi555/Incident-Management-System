from fastapi import Header, HTTPException, Request
from app.core.config import settings
import time

# Simple in-memory bucket for demonstration
class RateLimiter:
    def __init__(self, limit: int):
        self.limit = limit
        self.tokens = limit
        self.last_update = time.time()

    def consume(self):
        now = time.time()
        # Replenish tokens based on time passed
        self.tokens += (now - self.last_update) * self.limit
        if self.tokens > self.limit:
            self.tokens = self.limit
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

limiter = RateLimiter(settings.RATE_LIMIT_PER_SEC)

async def check_rate_limit():
    if not limiter.consume():
        raise HTTPException(status_code=429, detail="Global Rate Limit Exceeded")

async def validate_api_key(x_ims_key: str = Header(...)):
    # In production, check against a secret or database
    if x_ims_key != "sre-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")