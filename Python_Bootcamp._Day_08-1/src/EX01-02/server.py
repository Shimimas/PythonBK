from fastapi import FastAPI, Response
import enum
import pydantic
import typing
import uuid
import asyncio
import httpx
import json

app = FastAPI()

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
            resulted_code = ""
            try:
                r = await client.get(url)
                resulted_code = str(r.status_code)
            except Exception as e:
                resulted_code = str(e)
            self.result.append((url, resulted_code))

        async with httpx.AsyncClient() as client:
            tasks = [querry(client, url) for url in self.urls]
            await asyncio.gather(*tasks)

    async def start_task(self):
        self.status = TaskStatus.RUNNING
        await self.query_urls()
        self.status = TaskStatus.READY

running_tasks = set()
tasks: typing.Dict[uuid.UUID, Task] = {}

@app.post("/api/v1/tasks", status_code=httpx.codes.CREATED)
async def create_task(data: ListOfURLs):
    task = Task(urls=data.urls)
    tasks[task.id] = task
    async_task = asyncio.create_task(task.start_task())
    async_task.add_done_callback(lambda t=async_task : running_tasks.discard(t))
    running_tasks.add(async_task)
    return {"id": task.id}

@app.post("/api/v1/tasks/{task_id}", status_code=httpx.codes.OK)
async def check_task(task_id: uuid.UUID):
    try:
        task = tasks[task_id]
    except KeyError:
        return Response(status_code=404, content="Task is not found")
    if task.status != TaskStatus.READY:
        return Response(status_code=422, content="Task is not ready")
    data = json.dumps(task.result)
    tasks.pop(task_id)
    return data