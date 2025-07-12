from pydantic import BaseModel


class RoleUpdate(BaseModel):
    role: str  # "user" or "admin"
