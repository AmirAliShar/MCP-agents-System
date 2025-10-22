from pydantic import BaseModel,Field,field_validator
from datetime import date as DateType

# ---------- Pydantic Schemas ----------
class CustomerCreate(BaseModel):
    #id: int = Field(..., description="Unique ID for the customer")
    name: str = Field(..., min_length=2, max_length=100)
    date: str = Field(..., description="Date in ISO format YYYY-MM-DD")

    @field_validator("date")
    def validate_date(cls, value):
        # Ensure proper date format
        try:
            DateType.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError("Date must be in ISO format YYYY-MM-DD")


class CustomerRead(BaseModel):
    name: str
    date: str
