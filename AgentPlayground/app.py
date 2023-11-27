from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from agent import agent_executor
import logging

async def aprocess_input(input_text):
    print("aprocess_input started")
    input_dict = {"input": input_text}
    all_content = ""
    async for chunk in agent_executor.astream(input_dict):
        print(f"Received chunk: {chunk}")
        if chunk:
            # Extract 'output' value if chunk is a dictionary
            if isinstance(chunk, dict) and 'output' in chunk:
                chunk = chunk['output']
            all_content += chunk
            print(f"Yielding chunk: {all_content}")
            yield all_content
    print("aprocess_input finished")

app = FastAPI()

@app.get("/")
async def web_app() -> HTMLResponse:
    """
    Web App
    """
    with open("index.html") as f:
        html = f.read()
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received text data: {data}")
        async for chunk in aprocess_input(data):
            print(f"Sending chunk: {chunk}")
            await websocket.send_text(chunk)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )