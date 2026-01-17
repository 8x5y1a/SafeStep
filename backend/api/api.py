from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
connected_clients: list[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.post("/broadcast")
async def broadcast():
    print("broadcast")
    print(connected_clients)
    for ws in connected_clients:
        await ws.send_text("test")
