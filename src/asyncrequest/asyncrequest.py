"""
Module makes concurrent/async api calls to server
There are two modes to use this
When you have the same host/server then you can pass in the param base_url while creating an Instance of AsyncRequest()
and base_url will be appended to all the urls you pass to the call_apis method
example 1->
When the host/server is same this will provide you the best performance because there is also network optimization done
which will use the underlying session created for the first request.
#imporing stuff
import AsyncRequest, Request, Method

#make api calls
req_list = []
request = AsyncRequest(base_url='https://www.example.com')
req = Request(
            url=f'{api_url}/employee',
            method=Method.GET
        )
req_list.append(req)
response = request.call_apis(req_list)

example 2->

When the host/server is different you can make max 500(number may vary depending on the system and environment)
api calls using this since there are some
limitations on the number of ports/connection you can open from your system

#imporing stuff
import AsyncRequest, Request, Method

#make api calls
req_list = []
request = AsyncRequest()
req = Request(
            url='https://www.example.com',
            method=Method.GET
        )
req_list.append(req)
response = request.call_apis(req_list)
"""

import aiohttp
import asyncio
import json
import logging
import traceback
from enum import Enum
from abc import ABC, abstractmethod
from aiohttp import ClientSession

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

__author__ = 'aayushpllwr@gmail.com'
__version__ = 1.0


class MultiRequestError(Exception):
    pass


# TODO
class ServerOverloadError(Exception):
    pass


class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class Request(object):

    def __init__(self, url, method, headers=None, query_params=None, body=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.query_params = query_params
        self.body = body

    url: str
    headers: dict
    query_params: dict
    body: dict
    method: Method


class AsyncHelper:
    def __init__(self):
        self.tasks = []

    def add_to_queue(self, coro):
        self.tasks.append(asyncio.create_task(coro))

    async def execute_all(self):
        results = await asyncio.gather(*self.tasks)
        return results


class IAsyncRequest(ABC):

    def __init__(self, async_helper: AsyncHelper, base_url=None, retries=0):
        self.results = list()
        self.async_helper = async_helper
        self.base_url = base_url
        self.retries = retries

    @abstractmethod
    def make_async_calls(self, requests: list):
        pass


class AsyncRequest(IAsyncRequest):

    def __init__(self, async_helper=AsyncHelper(), base_url=None, retries=0):
        super().__init__(async_helper, base_url, retries)
        self.results = list()
        self.async_helper = async_helper
        self.base_url = base_url

    async def __make_call(self, request: Request):
        logger.debug(request)
        try:
            async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False),
                    headers=request.headers, trust_env=True
            ) as client:
                return await self.__decide_call_type(client, request)

        except Exception as exe:
            error = {
                'error': 'Api call for url failed',
                'url': request.url,
                'method': request.method.value,
                'traceback': traceback.format_exc()
            }
            raise MultiRequestError(error) from exe

    async def __make_call_same_host(self, request: Request, client: ClientSession):
        logger.debug(request)
        try:
            return await self.__decide_call_type(client, request)
        except Exception as exe:
            error = {
                'error': 'Api call for url failed',
                'url': request.url,
                'method': request.method.value,
                'traceback': traceback.format_exc()
            }
            raise MultiRequestError(error) from exe

    async def __decide_call_type(self, client: ClientSession, request: Request):
        if request.method == Method.GET:
            async with client.get(url=request.url, params=request.query_params) as resp:
                return resp

        elif request.method == Method.POST:
            async with client.post(
                    url=request.url,
                    params=request.query_params,
                    data=self.convert_body(request.body)
            ) as resp:
                return resp

        elif request.method == Method.PUT:
            async with client.put(
                    url=request.url,
                    params=request.query_params,
                    data=self.convert_body(request.body)
            ) as resp:
                return resp

        elif request.method == Method.PATCH:
            async with client.patch(
                    url=request.url,
                    params=request.query_params,
                    data=self.convert_body(request.body)
            ) as resp:
                return resp

        elif request.method == Method.DELETE:
            async with client.delete(url=request.url, params=request.query_params) as resp:
                return resp

        else:
            return None

    async def make_async_calls(self, requests: list):
        if self.base_url:
            async with aiohttp.ClientSession(
                    base_url=self.base_url,
                    connector=aiohttp.TCPConnector(verify_ssl=False),
                    headers=requests[0].headers, trust_env=True
            ) as same_client:
                for req in requests:
                    self.async_helper.add_to_queue(self.__make_call_same_host(req, same_client))
                response = await self.async_helper.execute_all()
                return response

        else:
            for req in requests:
                self.async_helper.add_to_queue(self.__make_call(req))
            response = await self.async_helper.execute_all()
            return response

    def call_apis(self, requests: list):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(self.make_async_calls(requests))

    @staticmethod
    def convert_body(body):
        try:
            return json.dumps(body)
        except Exception as exe:
            logger.error('could not convert body to string', body)
