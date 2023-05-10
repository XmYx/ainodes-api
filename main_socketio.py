import subprocess

import socketio

from nodes import Graph, DEBUG, create_pack

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# wrap with ASGI application
app = socketio.ASGIApp(sio)


@sio.on('send')
async def send_images(sid, node_id, images):
    for image in images:
        pack = create_pack(image, node_id)
        await sio.emit('message', pack, room=sid)
@sio.on('*')
async def catch_all(event, sid, data):
    graph = Graph(sio, sid, send_images)
    print(data)
    if event in ["sync", "execute"]:
        graph.sync(data)
        await graph.run(data[0]['id'])
    pass

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == "__main__":
    subprocess.call(["uvicorn", "main_socketio:app", "--proxy-headers", "--host", "127.0.0.1", "--port", "3001"])

