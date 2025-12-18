from fastapi import FastAPI

from api.routers import heroes,weapons,inventories

app = FastAPI()

app.include_router(heroes.router)
app.include_router(inventories.router)
app.include_router(weapons.router)

