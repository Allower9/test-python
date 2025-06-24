import asyncpg
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = "postgresql://myappuser:secretpassword@192.168.1.126:5432/myappdb"

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/")
async def read_root():
    row = await app.state.db.fetchrow("SELECT 'Hello from PostgreSQL!' AS message;")
    return {"message": row["message"]}

