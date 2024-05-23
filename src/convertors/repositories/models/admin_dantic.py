from pydantic import BaseModel

class AdminDantic(BaseModel):
    
    id: int
    name: str
    password: str
    email: str