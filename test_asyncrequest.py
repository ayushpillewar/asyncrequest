import unittest
from asyncrequest import AsyncRequest, Request, Method
import asyncio


api_url = 'https://www.boredapi.com/api/activity'


class MyTestCase(unittest.TestCase):
    def test_api_calls(self):
        req = Request(
            url=api_url,
            method=Method.GET
        )
        req_list = [req]

        request = AsyncRequest()
        response = asyncio.run(request.make_async_calls(req_list))
        print(response)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
