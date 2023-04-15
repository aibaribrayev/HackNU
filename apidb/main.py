from fastapi import FastAPI
from app.interfaces.routers import products, zakupki, sales
from app.infrastructure.db import engine, Base

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(products.router)
app.include_router(zakupki.router)
app.include_router(sales.router)
