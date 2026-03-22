import asyncio
import websockets
import json

connected = set()

async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            # broadcast to all other connected clients
            others = {ws for ws in connected if ws != websocket}
            if others:
                await asyncio.gather(*[ws.send(message) for ws in others], return_exceptions=True)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.discard(websocket)

async def main():
    async with websockets.serve(handler, '0.0.0.0', 10000):
        await asyncio.Future()

asyncio.run(main())
