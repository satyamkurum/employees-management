from fastapi import Depends
from app.auth import get_current_user
from fastapi import APIRouter, HTTPException, status
from datetime import datetime 
from app.database import employee_collection
from app.models import EmployeeSchema, employee_helper
from app.models import UpdateEmployeeSchema 
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Query

router = APIRouter()

@router.post(
    "/",
    response_description="Add a new employee",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee: EmployeeSchema,
    current_user: dict = Depends(get_current_user) 
):
    """
    Insert a new employee record into the database.
    """
    
    existing_employee = await employee_collection.find_one(
        {"employee_id": employee.employee_id}
    )
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID {employee.employee_id} already exists."
        )

    employee_dict = employee.model_dump()
    employee_dict["joining_date"] = datetime.combine(employee.joining_date, datetime.min.time())

    new_employee = await employee_collection.insert_one(employee_dict)

    created_employee = await employee_collection.find_one(
        {"_id": new_employee.inserted_id}
    )
    return employee_helper(created_employee)

@router.get(
    "/",
    response_description="List employees with optional filtering, sorting, and pagination",
    response_model=List[dict]
)
async def list_employees(
    department: Optional[str] = None,
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, gt=0, le=100, description="Maximum number of records to return")
):
    """
    List employees with pagination, optional filtering by department,
    and sorted by joining_date (newest first).
    """
    query = {}
    if department:
        query["department"] = department

    employees_cursor = employee_collection.find(query).sort("joining_date", -1).skip(skip).limit(limit)
    
    employees = [employee_helper(employee) async for employee in employees_cursor]
    return employees


@router.get(
    "/{employee_id}",
    response_description="Get a single employee by their ID",
    response_model=dict
)
async def get_employee(employee_id: str):
    """
    Find and return an employee record by their unique employee_id.
    """
    employee = await employee_collection.find_one({"employee_id": employee_id})

    if employee:
        return employee_helper(employee)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with ID {employee_id} not found."
    )


@router.put(
    "/{employee_id}",
    response_description="Update an employee's details",
    response_model=dict
)
async def update_employee(
    employee_id: str,
    update_data: UpdateEmployeeSchema,
    current_user: dict = Depends(get_current_user) 
):
    """
    Update an existing employee's record.
    """
    update_fields = update_data.model_dump(exclude_unset=True)

    if len(update_fields) >= 1:
        result = await employee_collection.update_one(
            {"employee_id": employee_id}, {"$set": update_fields}
        )

        if result.matched_count == 1:
            updated_employee = await employee_collection.find_one(
                {"employee_id": employee_id}
            )
            return employee_helper(updated_employee)

    existing_employee = await employee_collection.find_one({"employee_id": employee_id})
    if existing_employee:
        return employee_helper(existing_employee)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with ID {employee_id} not found."
    )


@router.delete(
    "/{employee_id}",
    response_description="Delete an employee from the database"
)
async def delete_employee(
    employee_id: str,
    current_user: dict = Depends(get_current_user) 
):
    """
    Delete an employee record by their unique employee_id.
    """
    result = await employee_collection.delete_one({"employee_id": employee_id})

    if result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Employee with ID {employee_id} deleted successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with ID {employee_id} not found."
    )


@router.get(
    "/avg-salary/by-department",
    response_description="Get the average salary grouped by department",
    response_model=List[dict]
)
async def get_average_salary_by_department():
    """
    Calculates the average salary for each department using an aggregation pipeline.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "department": "$_id",
                "avg_salary": 1,
                "_id": 0
            }
        }
    ]
    
    result_cursor = employee_collection.aggregate(pipeline)
    result = [doc async for doc in result_cursor]
    
    if result:
        return result
    
    return []


@router.get(
    "/search/",
    response_description="Search for employees by skill",
    response_model=List[dict]
)
async def search_employees_by_skill(skill: str):
    """
    Find all employees who possess a given skill.
    """
    query = {"skills": skill}
    employees_cursor = employee_collection.find(query)
    
    employees = [employee_helper(employee) async for employee in employees_cursor]
    
    return employees