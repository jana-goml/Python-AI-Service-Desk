from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.ticket_routes import router
from app.core.database import AsyncSessionLocal, Base
from app.core.database import engine
import app.middleware.response_time as response_time_middleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import TicketNotFoundError
from app.api.ai import router as ai_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

app = FastAPI(app_name="AI Service Desk",lifespan=lifespan)

app.middleware("http")(response_time_middleware.response_time_middleware)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(request:Request,exc:TicketNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "ticket_not_found",
            "id": exc.ticket_id,
        },
    )

@app.get("/ready")
async def ready():
    return {
        "status": "ready"
    }

@app.get("/health")
async def health():
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(
                text("SELECT 1")
            )
        return {
            "status": "healthy"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
    
app.include_router(router)
app.include_router(ai_router)
