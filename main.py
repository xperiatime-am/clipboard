from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = []

@app.get("/")
def read_root():
    return {"status": "clipboard server running"}

@app.get("/ui", response_class=HTMLResponse)
def ui():
    with open("/home/ubuntu/app/index.html") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            data = await ws.receive_text()

            for client in clients:
                if client != ws:
                    await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(ws)
