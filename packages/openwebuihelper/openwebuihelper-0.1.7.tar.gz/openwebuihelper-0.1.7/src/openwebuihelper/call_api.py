from aiohttp import ClientSession
from typing import Dict, Any
from json import dumps




async def call_api(url: str, method: str = 'post', body: Any = None,  params: Dict[str, Any] = None, headers: Dict[str, Any] = None):
    try:
        async with ClientSession() as session:
            methodFunc = session.get
            if method == 'post':
                methodFunc = session.post

            async with methodFunc(url, params=params, headers=headers, data=dumps(body)) as response:
                if response.status == 200:
                    contentType = response.headers.get('Content-Type')

                    if 'text/event-stream;' in contentType:
                        return await response.text()
                    elif 'application/json' in contentType:
                        return await response.json()

    except Exception as e:
        raise e