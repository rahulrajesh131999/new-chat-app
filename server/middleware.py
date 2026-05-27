from fastapi import Request

async def middleware(request:Request, call_next):
    return None