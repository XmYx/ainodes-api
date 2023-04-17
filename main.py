import subprocess
import threading

from fastapi import FastAPI
from starlette.websockets import WebSocket

import msgpack

from nodes import Graph

app: FastAPI = FastAPI()

import base64


lock = threading.Lock()


@app.websocket("/ws/nodes")
async def websocket_node_sync(websocket: WebSocket):
    """
    Main Loop to receive, and process nodegraph requests

    :param websocket:
    :param websocket_id:
    :return:
    """

    graph = Graph(websocket)

    await websocket.accept()
    while True:
        data = await websocket.receive()
        data = msgpack.unpackb(data['bytes'], raw=False)
        if data['task'] == 'sync':
            graph.sync(data['values'])
        elif data['task'] == 'eval':
            await graph.run(data['values'][0]['id'])


if __name__ == "__main__":
    subprocess.run(["uvicorn", "main:app", "--proxy-headers", "--host", "127.0.0.1", "--port", "5003"])

