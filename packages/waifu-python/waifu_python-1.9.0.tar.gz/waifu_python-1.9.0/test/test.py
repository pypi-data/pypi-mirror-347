import asyncio
import iwara
from iwara import AsyncApiClient

async def main():
    client = AsyncApiClient("akoushik88@gmail.com", "SRaiden1@#")
    random_iwara = await iwara.fetch_random(sort='popularity', rating='ecchi', limit=16)
    print(random_iwara)

asyncio.run(main())
