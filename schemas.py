from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

# Example schemas kept for reference but not used by the app right now
class User(BaseModel):
    name: str
    email: str
    address: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

# Application schema: each class maps to a collection with its lowercase name
class Task(BaseModel):
    """
    Tasks collection schema (collection name: "task")
    """
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Details of the task")
    assigned_to: str = Field(..., description="Assignee name")
    customer: Optional[str] = Field(None, description="Customer name/tag")
    supplier: Optional[str] = Field(None, description="Supplier name/tag")
    project: Optional[str] = Field(None, description="Project tag")
    priority: Literal['High', 'Medium', 'Low'] = Field('Medium', description="Task priority")
    status: Literal['Pending', 'In Progress', 'Done'] = Field('Pending', description="Workflow status")
    due_date: Optional[str] = Field(None, description="Due date label (e.g., '2025-11-05' or 'Today')")
    notes: Optional[str] = Field(None, description="Additional notes")
    recurring: Optional[Literal['none', 'daily', 'weekly', 'monthly']] = Field('none', description="Recurring pattern")
