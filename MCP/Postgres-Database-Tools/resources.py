from fastmcp import FastMCP

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

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
engine =create_engine(url=DB)
Base =declarative_base()

mcp =FastMCP(name="Resources")

@mcp.resource("resource://expensive")
def get_expensive_data() -> list[dict]:
    """Return all expense data (read-only resource)."""
    try:
        with Session(bind=engine) as session:
            data = session.query(ExpensiveTracker).all()
            return [
                {
                    "id": item.id,
                    "date": item.date.isoformat(),
                    "education": item.education,
                    "travel": item.travel,
                    "food": item.food,
                    "fruit": item.fruit,
                    "tution": item.tution,
                    "health": item.health,
                }
                for item in data
            ]
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__=="__main__":
    init_database()
    mcp.run(transport ="streamable-http",port=8001)
# For Run
"""
uv run resources.py
uv run fastmcp dev resources.py
"""