from fastapi import APIRouter, HTTPException, status, Query, Depends
from app.auth import get_current_user
from fastapi import FastAPI, HTTPException
from app.database import database
from app.routers.employee import router as employee_route
from app.routers.auth import router as auth_router

app = FastAPI(title="Employee Management API")

app.include_router(auth_router, tags=["Authentication"])
app.include_router(employee_route, tags=["Employees"], prefix="/employees")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Employee Management System!"}


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Checks the connection to the database."""
    try:
        await database.command('ping')
        return {"status": "ok", "message": "Successfully connected to the database."}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")