#!.venv/bin/python3.10
from fastapi import FastAPI, Response
import pydantic
import uuid
import httpx
import typing
import enum
import asyncio
import json
import logging
import aioredis
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

app = FastAPI()
redis = aioredis.from_url("redis://localhost")
CACHE_CLEAR_INTERVAL_SEC = 30

def add_background_task(coroutine : typing.Coroutine):
    task = asyncio.create_task(coroutine)
    running_tasks.add(task)
    task.add_done_callback(lambda t=task: running_tasks.discard(t))

async def clean_redis_cache():
    while True:
        await asyncio.sleep(CACHE_CLEAR_INTERVAL_SEC)
        logging.info("Clearing Redis cache")
        async for key in redis.scan_iter("CACHE:*"):
            await redis.delete(key)

class TaskStatus(enum.Enum):
    NOT_STARTED = 'not_started'
    RUNNING = 'running'
    READY = 'ready'
    
class ListOfURLs(pydantic.BaseModel):
    urls: typing.List[str]

class Task(pydantic.BaseModel):
    id: uuid.UUID = uuid.uuid4()
    urls: typing.List[str]
    status: TaskStatus = TaskStatus.NOT_STARTED
    result: typing.List[typing.Tuple[str, str]] = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def query_urls(self):
        async def querry(client, url):
            logging.debug(f"Querying {url}")
            resulted_code = ""
            try:
                domain = urlparse(url).netloc
                if domain:
                    count = await redis.incr(f"CACHE:{domain}_count")
                    logging.info(f"Cached counter for domain: {domain} - {count}")
                resulted_code: str = ""
                cached_value: bytes = await redis.get(f"CACHE:{url}")
                if cached_value is None:
                    logging.info(f"No cache for url: {url}")
                    r = await client.get(url)
                    resulted_code = str(r.status_code)
                    await redis.set(f"CACHE:{url}", str(resulted_code))
                else:
                    resulted_code = cached_value.decode('utf-8')
                    logging.info(f"Cached result code found for url: {url} - {resulted_code}")
            except Exception as e:
                resulted_code = repr(e)
            self.result.append((url, resulted_code))
            logging.debug(f"Received code: {resulted_code}")
        async with httpx.AsyncClient() as client:
            tasks = [querry(client, url) for url in self.urls]
            await asyncio.gather(*tasks)

    async def start_task(self):
        logging.debug(f"Task with id: {self.id} started")
        self.status = TaskStatus.RUNNING
        await self.query_urls()
        self.status = TaskStatus.READY
        logging.debug(f"Task with id: {self.id} finished")
    
running_tasks = set()
tasks: typing.Dict[uuid.UUID, Task] = {}
add_background_task(clean_redis_cache())

@app.post("/api/v1/tasks", status_code=httpx.codes.CREATED)
async def create_task(data: ListOfURLs):
    task = Task(urls=data.urls)
    tasks[task.id] = task
    add_background_task(task.start_task())
    return {"id": task.id}

@app.post("/api/v1/tasks/{task_id}", status_code=httpx.codes.OK)
async def check_task(task_id: uuid.UUID):
    try:
        task = tasks[task_id]
    except KeyError:
        logging.warning(f"Task with id: {task_id} not found")
        return Response(status_code=404, content="Task is not found")
    if task.status != TaskStatus.READY:
        logging.debug(f"Task with id: {task_id} not ready")
        return Response(status_code=422, content="Task is not ready")
    data = json.dumps(task.result)
    logging.debug(f"Task with id: {task_id} returning result")
    tasks.pop(task_id)
    return data