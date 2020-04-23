# Name: Post Request
# Author: James Tang
# Date: 23/04/2020
# Description: Submits a request about a pump and dump to the database.

import requests

class PostRequest:
    def submitRequest(self, msg: str):
        body = {'data_1': msg,
                'data_2': 'j22',
                'data_3': 'jk3d',
                'data_4': 'j224a',
                'email': 'jameskibi@gmail.com',
                'password': '123456',
                'name': 'James'}
        r = requests.post('http://localhost:5000/api/pumpbot', json=body)
        print(r.text)

