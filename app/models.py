from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class EmployeeSchema(BaseModel):
    employee_id: str = Field(..., description="Unique identifier for the employee")
    name: str = Field(..., description="Full name of the employee")
    department: str = Field(..., description="Department the employee belongs to")
    salary: float = Field(..., gt=0, description="Salary of the employee")
    joining_date: date = Field(..., description="Date the employee joined")
    skills: List[str] = Field(..., description="List of employee's skills")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "E456",
                "name": "Satyam Kurum",
                "department": "AI Engineer",
                "salary": 1200000,
                "joining_date": "2025-10-01",
                "skills": ["Machine Learrning", "AI Agent Development", "Python", "FastAPI", "MongoDB", "Langchain"]
            }
        }

class UpdateEmployeeSchema(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Royal",
                "salary": 65000
            }
        }

def employee_helper(employee) -> dict:
    """It Transforms a database record (BSON) into a Python dictionary."""
    return {
        "id": str(employee["_id"]),
        "employee_id": employee["employee_id"],
        "name": employee["name"],
        "department": employee["department"],
        "salary": employee["salary"],
        "joining_date": str(employee["joining_date"]),
        "skills": employee["skills"],
    }