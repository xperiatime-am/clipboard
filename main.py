from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

clients = []

# =====================
# REDIRECT HOME
# =====================
@app.get("/")
def root():
    return FileResponse("static/home.html")

# =====================
# HOME PAGE
# =====================
@app.get("/home")
def home():
    return FileResponse("static/home.html")

# =====================
# UI CLIPBOARD
# =====================
@app.get("/ui", response_class=HTMLResponse)
def ui():
    with open("index.html", "r") as f:
        return f.read()

# =====================
# STATUS API
# =====================
@app.get("/api")
def api():
    return {"status": "ok", "app": "clipboard-sync"}

# =====================
# WEBSOCKET
# =====================
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
