from . import AsyncZenbrokerClient
import asyncio


client = AsyncZenbrokerClient(
    base_url="https://broker.awsp.oraczen.xyz",
    application_id="piyush"
)


async def cb(message):
    print(message)

client.on_message(callback=cb)

async def main():
    await client.connect()
    await client.subscribe(channel="test")
    await client.listen()


asyncio.run(main())