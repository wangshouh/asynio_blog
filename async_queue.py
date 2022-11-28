import aiohttp
import asyncio
import time
from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def exact_rec_book(raw_html: str, q: asyncio.Queue) -> str:
    soup = BeautifulSoup(raw_html, 'lxml')
    rec_div = soup.find(id="db-rec-section")
    for dt in rec_div.find_all("dt"):
        url = dt.find("a").get("href")
        print(url)
        if url:
            await q.put(url)
        else:
            pass


async def crawler(name: int, s: ClientSession, q: asyncio.Queue) -> None:
    url = await q.get()
    req = await s.get(url)
    html = await req.text()
    await exact_rec_book(html, q)


async def main():
    q = asyncio.Queue()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.5,zh-TW;q=0.3,zh-HK;q=0.2',
    }
    await q.put("https://book.douban.com/subject/35196328/")
    async with ClientSession(headers=headers) as session:
        task = [crawler(name, session, q) for name in range(5)]
        await asyncio.gather(*task)


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Code runtime: {elapsed}")
