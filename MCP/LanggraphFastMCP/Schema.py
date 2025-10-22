from pydantic import BaseModel

class State(BaseModel):
    text:str
    max_len:str

class OutPutState(BaseModel):
    summary:str