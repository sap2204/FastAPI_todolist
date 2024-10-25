from fastapi import FastAPI
from app.users.router import router as router_user
from app.tasks.router import router as router_task


app = FastAPI()


app.include_router(router_user)
app.include_router(router_task)