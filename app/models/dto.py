from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    login: str
    password: str
