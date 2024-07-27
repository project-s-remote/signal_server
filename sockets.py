import socketio
import uuid
from mongodb import client

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['*'],  # 모든 origin 허용
    engineio_logger=True  # 디버깅을 위해 로깅 활성화
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='/ws/socket.io'
)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connected', {'message': 'Connected successfully', 'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def signal(sid, data):
    # print(data)
    await sio.emit('signal', data, room=data.get('sid'))

@sio.event
async def mouse_move(sid, data):
    print(data)
    await sio.emit('mouse_move', data, room=data.get('sid'))

@sio.event
async def mouse_click(sid, data):
    # print(data)
    await sio.emit('mouse_click', data, room=data.get('sid'))
