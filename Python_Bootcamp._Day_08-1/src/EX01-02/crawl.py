import httpx
import typing
import argparse
import json
import asyncio


HOST='localhost:8888'

def parse_args() -> typing.List[str]:
    """Parses args and os env to get required settings"""
    parser = argparse.ArgumentParser(description="Crawl client", add_help=True)
    parser.add_argument('files', metavar='urls', type=str, nargs='+', help='URLs to send')
    parsed = parser.parse_args()
    urls = getattr(parsed, 'files', [])
    return (urls)
    

async def send_urls(urls: typing.List[str]):
    data = {'urls': urls}
    data = json.dumps(data)
    async with httpx.AsyncClient() as client:
        r = await client.post(f"http://{HOST}/api/v1/tasks", data=data)
        if r.status_code != httpx.codes.CREATED:
            exit(1)
        task_id = r.json()['id']
        print(task_id)
        r = await client.post(f"http://{HOST}/api/v1/tasks/{task_id}")
        while r.status_code != httpx.codes.OK:
            if (r.status_code == httpx.codes.REQUEST_TIMEOUT
                or r.status_code == httpx.codes.NOT_FOUND):
                exit(1)
            await asyncio.sleep(1)
            r = await client.post(f"http://{HOST}/api/v1/tasks/{task_id}")
        url_data: typing.List[typing.Tuple[str, int]] = json.loads(r.json())
        for url, code in url_data:
            print(f"{url} - {code}")
    
if __name__ == '__main__':
    urls = parse_args()
    asyncio.run(send_urls(urls))