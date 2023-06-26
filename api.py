import redis
from fastapi import FastAPI
from typing import Union

import os
redis_url = os.environ.get('REDIS_URL')
if redis_url is None:
    redis_url = "redis://localhost:6379"
print("Connecting to redis at " + redis_url)
r = redis.Redis.from_url(redis_url, decode_responses=True)
ts = r.ts()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Success. Try /ethereum/latest"}


@app.get("/ethereum/latest")
def read_root():
    sample_safe = ts.get("ethereum-safe")
    sample_propose = ts.get("ethereum-propose")
    sample_fast = ts.get("ethereum-fast")
    return {"message":"Success", "safe": sample_safe, "propose": sample_propose, "fast": sample_fast}

