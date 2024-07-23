import socketio
import uuid

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='sockets'
)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


rooms = {}


@sio.event
async def join_room(sid, data):
    room_id = data['room_id']
    if room_id not in rooms:
        rooms[room_id] = set()
    rooms[room_id].add(sid)
    await sio.enter_room(sid, room_id)

    print("입장")

    if len(rooms[room_id]) >= 2:  # 두 명이 룸에 입장하면
        await sio.emit('ready_for_connection', room=room_id)


@sio.event
async def offer(sid, data):
    room_id = data['room_id']
    await sio.emit('offer', {'offer': data['offer']}, room=room_id, skip_sid=sid)


@sio.event
async def answer(sid, data):
    room_id = data['room_id']
    await sio.emit('answer', {'answer': data['answer']}, room=room_id, skip_sid=sid)


@sio.event
async def ice_candidate(sid, data):
    room_id = data['room_id']
    await sio.emit('ice_candidate', {'candidate': data['candidate']}, room=room_id, skip_sid=sid)
