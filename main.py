from fastapi import FastAPI
from routers.user import user_router
from routers.notes import notes_router


app = FastAPI()

app.include_router(user_router,prefix="/api/v1", tags=["users"])
app.include_router(notes_router , prefix="/api/v1", tags=["notes"])