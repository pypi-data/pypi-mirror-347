import asyncio
import pytest

from typing import Dict, Any

from src import call_api, call_api_stream

async def call1():
    url = f"https://aigateway.app.swirecocacola.com/api/v1/services/aigc/text2image/image-synthesis"
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 0xxwjj3H4U8swCQo",
        "X-DashScope-Async": "enable"
    }
    body = {
        "model": "wanx2.1-t2i-turbo",
        "input": {
            "prompt": "夏日雪碧"
        },
        "parameters": {
            "size": "1024*1024",
            "n": 1
        }
    }
    
    res1 = await call_api(url=url, headers=headers, body=body)
    task_id = res1.get('output').get('task_id')

    await asyncio.sleep(10)

    res2 = await call_api(url=f'https://aigateway.app.swirecocacola.com/api/v1/tasks/{task_id}', headers={
        "Authorization": "Bearer 0xxwjj3H4U8swCQo",
    }, method='get' )

    print('res2', res2)


async def call2():
    url = f"https://aigateway.app.swirecocacola.com/api/v1/apps/34d49fe34eed420db309a6cdecd8e040/completion"
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 0xxwjj3H4U8swCQo",
        "X-DashScope-SSE": "enable"
    }
    body = {
        "input": {
            "prompt": "你是谁？"
        },
        "parameters": {
            "has_thoughts": True,
            "incremental_output": True,
        },
        "debug": {}
    }
    
    
    res = call_api_stream(url=url, headers=headers, body=body)
    async for r in res:
        print(r)



def test_1():
    asyncio.run( call1() )

def test_2():
    asyncio.run( call2() )