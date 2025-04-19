from api import router

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lawly User API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

