import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f'<< {name}')

    await websocket.send(name)
    print(f">> echo: {name}")

async def main():
    async with websockets.serve(hello, "172.20.10.3", 6666):
        await asyncio.Future()  # run forever

asyncio.run(main())
