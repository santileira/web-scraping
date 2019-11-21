import aiohttp
from bs4 import BeautifulSoup


async def get(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                text = await response.text()
                return BeautifulSoup(text, "html.parser")
            else:
                return None
    except Exception as ex:
        print(f'Error during requests to {url} : {str(ex)}')
        return None
