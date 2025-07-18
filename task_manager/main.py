from fastapi import FastAPI
from task_manager.core.routers import router as user_router
from task_manager.tasks.routers import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
