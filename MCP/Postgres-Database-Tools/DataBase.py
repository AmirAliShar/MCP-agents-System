from sqlalchemy import create_engine, Column, String, Integer, Date, extract
from sqlalchemy.orm import declarative_base
from datetime import date as DateType

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

# ---------- DATABASE INIT ----------
def init_database() -> None:
    try:
        Base.metadata.create_all(engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"Database init error: {e}")


# ---------- ORM MODEL ----------
class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)


class ExpensiveTracker(Base):
    __tablename__="expensivetracker"
    id = Column(Integer,primary_key=True,autoincrement=True)
    date = Column(Date,nullable =False)
    education = Column(Integer,nullable=False)
    travel = Column(Integer,nullable=False)
    food = Column(Integer,nullable=False)
    fruit = Column(Integer,nullable = False)
    tution = Column(Integer,nullable =False)
    health = Column(Integer,nullable =False)
