from datetime import datetime

from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    user_id: int | None = None
    created_by_id: int | None = None

class TaskUpdate(TaskCreate):
    name: str | None = None

class TaskRead(TaskUpdate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
