from fastapi import WebSocket, WebSocketDisconnect, Cookie, HTTPException, Depends, status
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.room import Room
from app.models.room_user import RoomUser
from uuid import UUID
import json


router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # {room_number: [websockets]}
        self.room_users = {}  # {room_number: [user_ids]}

    async def connect(self, websocket: WebSocket, room_number: str, user_id: UUID, db: Session):
        await websocket.accept()

        # Add the user to the room
        if room_number not in self.room_users:
            self.room_users[room_number] = []
        self.room_users[room_number].append(user_id)

        # Add the WebSocket connection
        if room_number not in self.active_connections:
            self.active_connections[room_number] = []
        self.active_connections[room_number].append(websocket)

        # Broadcast the updated user list
        await self.broadcast_user_list(room_number, db)

    def disconnect(self, websocket: WebSocket, room_number: str, user_id: UUID, db: Session):
        if room_number in self.active_connections:
            self.active_connections[room_number].remove(websocket)

        # Remove the user from the room
        if room_number in self.room_users and user_id in self.room_users[room_number]:
            self.room_users[room_number].remove(user_id)

        # Broadcast the updated user list
        if room_number in self.room_users and not self.room_users[room_number]:
            del self.room_users[room_number]

    async def broadcast_user_list(self, room_number: str, db: Session):
        if room_number in self.room_users:
            user_ids = self.room_users[room_number]
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            user_list = [{"id": str(user.id), "username": user.username} for user in users]

            # Broadcast the user list to all connected clients
            if room_number in self.active_connections:
                for connection in self.active_connections[room_number]:
                    await connection.send_text(json.dumps({"type": "user_list", "users": user_list}))

    async def broadcast_code_change(self, message: str, room_number: str):
        if room_number in self.active_connections:
            for connection in self.active_connections[room_number]:
                await connection.send_text(json.dumps({"type": "code_change", "content": message}))

manager = ConnectionManager()

@router.websocket("/ws/{room_number}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_number: str,
    access_token: str = Cookie(None),  # Extract the token from the cookie
    db: Session = Depends(get_db)
):
    if not access_token:
        # Reject the connection if the token is missing
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        # Decode the JWT token to get the user ID
        user_id = decode_token(access_token)
    except HTTPException as e:
        # Reject the connection if the token is invalid
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, room_number, user_id, db)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast code changes to all connected clients
            await manager.broadcast_code_change(data, room_number)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_number, user_id, db)