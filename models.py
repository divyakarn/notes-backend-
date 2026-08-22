from pydantic import BaseModel
from datetime import datetime 


class CreateNotes(BaseModel):
    title: str
    content: str

class UpdateNotes(BaseModel):
    title: str = None
    content: str = None

class NotesResponse(CreateNotes):
    id : int
    owner_id: int
    created_at: datetime
    updated_at:datetime
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id: int
    username:str
    class Config :
        from_attribute = True






