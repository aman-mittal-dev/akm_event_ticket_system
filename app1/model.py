# app/models.py
from pydantic import BaseModel

class Ticket(BaseModel):
    ticket_id: str
    encrypted_data: str
    status: str = "unused"  # can be: unused / used
