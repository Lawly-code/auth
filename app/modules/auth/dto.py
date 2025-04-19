from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    login: str
    password: str


class RegisterUserDTO(BaseModel):
    name: str
    email: str
    password: str
    agree_to_terms: bool
