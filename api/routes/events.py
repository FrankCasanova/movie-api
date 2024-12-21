from sse_starlette.sse import EventSourceResponse
from api.shared_state import listeners
from fastapi import APIRouter
import asyncio

event_router = APIRouter()
event_router.prefix = "/events"

@event_router.get("/", response_class=EventSourceResponse)
async def sse_endpoint():
    async def event_generator():
        queue = asyncio.Queue()
        listeners.append(queue)
        try:
            while True:
                data = await queue.get()
                yield data
        except asyncio.CancelledError:
            listeners.remove(queue)
            raise

    return EventSourceResponse(event_generator())