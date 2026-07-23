import time 
from fastapi import Request

async def response_time_middleware(request:Request,call_next):
    start_time = time.perf_counter()
    res = await call_next(request)
    process_time = time.perf_counter() - start_time
    res.headers["Processing-Time"] = f"{process_time:.4f}s"
    return res