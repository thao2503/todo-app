from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import metadata
from routers import authentication, task, user
from config import settings
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan, root_path=settings.FASTAPI_ROOT_PATH)

app.include_router(user.router)
app.include_router(task.router)
app.include_router(authentication.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables() -> None:
    metadata.bind = engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)