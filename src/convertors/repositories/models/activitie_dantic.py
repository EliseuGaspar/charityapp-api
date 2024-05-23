from pydantic import BaseModel

class ActivitieDantic(BaseModel):
    """"""
    id: int
    user: str
    pdf_name: str
    date_activitie: str
    status: bool