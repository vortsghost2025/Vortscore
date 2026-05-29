#!/usr/bin/env python3
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"status": "Vitalis Core Active"}

@app.get("/stream")
async def stream():
    from src.comm.channel import channel
    import asyncio
    queue = asyncio.Queue()
    def _push(payload):
        asyncio.create_task(queue.put(payload))
    channel.subscribe("veritas_reply", _push)
    try:
        while True:
            payload = await queue.get()
            yield f"data: {json.dumps(payload)}\n\n"
    finally:
        channel._subscribers["veritas_reply"].remove(_push)
