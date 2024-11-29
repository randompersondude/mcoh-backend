import asyncio
import websockets

uri = "ws://localhost:6789"

async def hello():
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Server says: {response}")

asyncio.run(hello())
