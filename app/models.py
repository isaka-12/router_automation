from pydantic import BaseModel

class User(BaseModel):
    ip_address: str
    mac_address: str = None
    status: str = "pending"  # pending or allowed
