from sqlalchemy import (
    TIMESTAMP,Integer, String, Column
)
from datetime import datetime
from src.domain.configs.database import base


class Admin(base):
    """"""
    _objectID = 'admin'
    __tablename__ = 'admins'
    
    id = Column(Integer, nullable = False, unique = True, autoincrement = True, primary_key=True)
    name = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, nullable = False, default = datetime.now())

    def __init__(self, name: str, email: str, password: str):
        """"""
        self.name = name
        self.email = email
        self.password = password