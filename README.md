# ASYNCREQUEST

This module makes use of aiohttp to make api calls 
thanks to creator and contributor of that project 
https://github.com/aio-libs/aiohttp

Module makes concurrent/async api calls to server
There are two modes to use this
When you have the same host/server then you can pass in the param base_url while creating an Instance of AsyncRequest()
and base_url will be appended to all the urls you pass to the call_apis method


# example 1
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

# example 2

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