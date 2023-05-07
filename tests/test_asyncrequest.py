import unittest
from src.asyncrequest.asyncrequest import AsyncRequest, Request, Method
import requests
import time

api_url = '/api/activity'


class MyTestCase(unittest.TestCase):
    def test_api_calls(self):
        start = time.time()
        req = Request(
            url=api_url,
            method=Method.GET
        )
        req_list = []
        for i in range(10):
            req_list.append(req)

        request = AsyncRequest(base_url='https://www.boredapi.com')

        response = request.call_apis(req_list)
        end = time.time()
        print(response)
        print('time taken ', end - start)

        self.assertEqual(True, True)

    def test_api_with_normal(self):
        start = time.time()
        response = requests.get(url=api_url)
        print(response)
        end = time.time()
        print('time taken ', end - start)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
