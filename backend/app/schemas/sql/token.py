from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    sub: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
    
class Message(BaseModel):
    message: str

class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)