from pydantic import BaseModel


class RoomCreate(BaseModel):
    room_number: str

class RoomJoin(BaseModel):
    room_number: str