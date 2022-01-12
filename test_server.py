import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f'<< {name}')

    resp = 'Hello, STM!'
    await websocket.send(resp)
    print(f">> {resp}")

async def main():
    async with websockets.serve(hello, "localhost", 8001):
        await asyncio.Future()  # run forever

asyncio.run(main())