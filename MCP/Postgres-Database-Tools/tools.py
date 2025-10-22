from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult,TextContent

from datetime import date
from typing import List, Annotated

from sqlalchemy import create_engine, extract
from sqlalchemy.orm import declarative_base, Session
from datetime import date as DateType

from Schema import CustomerCreate,CustomerRead
from DataBase import Customer
from DataBase import init_database
from DataBase import ExpensiveTracker

import os
from dotenv import load_dotenv
load_dotenv()

# ---------- DATABASE SETUP ----------
PGDATABASE = os.environ.get("PGDATABASE")
PGPORT = os.environ.get("PGPORT")
PGUSER = os.environ.get("PGUSER")
PGHOST = os.environ.get("PGHOST")
PGPASSWORD = os.environ.get("PGPASSWORD")

DB = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
engine = create_engine(url=DB)
Base = declarative_base()


# ---------- MCP SERVER ----------
# Enable strict validation for this server
mcp = FastMCP(
    name="CustomerServer",
    # Configure behavior for duplicate tool names
    on_duplicate_tools="error",
    mask_error_details=True
    )


@mcp.tool(
    name="Customer_Support",           # Custom tool name for the LLM
    description="Search the customer name with optional month filtering.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "Amir Ali"}  # Custom metadata
)

def add_item(data: CustomerCreate) -> bool:
    """Insert a validated customer into the database"""
    try:
        with Session(bind=engine) as session:
            new_customer = Customer(
                
                name=data.name,
                date=DateType.fromisoformat(data.date),
            )
            session.add(new_customer)
            session.commit()
            return True 
    except Exception as e:
        print(f"Error: {e}")
        return False




@mcp.tool()
def get_item(month: str = "") -> List[CustomerRead]:
    """Get customers, optionally filtered by month"""
    try:
        with Session(bind=engine) as session:
            if month:
                month = int(month)
                result = (
                    session.query(Customer)
                    .filter(extract("month", Customer.date) == month)
                    .all()
                )
            else:
                result = session.query(Customer).all()

            return [
                CustomerRead(
                    name=c.name,
                    date=c.date.isoformat()
                )
                for c in result
            ]
    except Exception as e:
        print(f"Error: {e}")
        return []
    


# Expensive table
@mcp.tool(
        name="Expensive_Trackere",
        description="Add the expensive in the DataBase",
        meta={"version":"1.2","author":"Amir Ali"})
def Expensive(
    date:Annotated[date,"Date of the Month"],
    education:Annotated[int,"Monthly education expensive"],
    travel: Annotated[int,"Monthly travel expensive"],
    food: Annotated[int,"Monthly food expensive"],
    fruit: Annotated[int,"Monthly fruit expensive"],
    tution: Annotated[int,"Monthly tution expensive"],
    health: Annotated[int,"Monthly health expensive"]

    # You can also use the Field for strong validation or limit
)-> ToolResult:
    """Insert the data into Expensive Table"""
    try:
        
        with Session(bind=engine) as session:
            add_data= ExpensiveTracker(
                date=date,
                education=education,
                travel=travel,
                food=food,
                fruit=fruit,
                tution=tution,
                health=health

            )
            session.add(add_data)
            session.commit()
             
            #Structured Output object like result
            return ToolResult(
                content=[TextContent(type="text",text="Human-readable summary")],# This show in the unstructured block  
                structured_content={
                "date":date,
                "education" : education,
                "travel" : travel,
                "food" : food,
                "fruit" : fruit,
                "tuttion" : tution,
                "health" : health
                }
                )
    except Exception as e:
        print(e)
        return f"{e}"


if __name__ == "__main__":
    init_database()
    mcp.run(transport="streamable-http", port=8000)

# For Run
"""
uv run tools.py
uv run fastmcp dev tools.py
"""