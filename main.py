from fastapi import FastAPI
from routers import asset, attendance, project, user


app = FastAPI()






app.include_router(user.router)
app.include_router(asset.router)
app.include_router(attendance.router)
app.include_router(project.router)



