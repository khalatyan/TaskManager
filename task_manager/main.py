from fastapi import FastAPI
from task_manager.users.routers import router as user_router

app = FastAPI()

app.include_router(user_router)
