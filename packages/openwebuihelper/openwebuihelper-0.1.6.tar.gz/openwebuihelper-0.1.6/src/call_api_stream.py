from aiohttp import ClientSession
from typing import Dict, Any
from json import dumps, loads


async def call_api_stream(url: str, method: str = 'post', body: Any = None,  params: Dict[str, Any] = None, headers: Dict[str, Any] = None):
    try:
        async with ClientSession() as session:
            methodFunc = session.get
            if method == 'post':
                methodFunc = session.post

            async with methodFunc(url, params=params, headers=headers, data=dumps(body)) as response:
                if response.status == 200:
                    contentType = response.headers.get('Content-Type')

                    if 'text/event-stream;' in contentType:
                        async for line in response.content:
                            line_text = line.decode("utf-8")
                            if line_text.startswith("data:"):
                                yield loads(line_text[5:])
                    elif 'application/json' in contentType:
                        yield await response.json()

    except Exception as e:
        raise e