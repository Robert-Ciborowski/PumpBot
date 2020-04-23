# Name: Post Request
# Author: James Tang
# Date: 23/04/2020
# Description: Submits a request about a pump and dump to the database.

import json
import requests

class PostRequest:
    email: str
    password: str

    def __init__(self, botPropertiesFile="post_request_properties.json"):
        self._update_properties(botPropertiesFile)

    def submitRequest(self, msg: str):
        body = {'data_1': msg,
                'data_2': 'j22',
                'data_3': 'jk3d',
                'data_4': 'j224a',
                'email': self.email,
                'password': self.password,
                'name': 'James'}
        r = requests.post('http://localhost:5000/api/pumpbot', json=body)
        print(r.text)

    def _update_properties(self, propertiesPath: str) -> str:
        try:
            with open(propertiesPath, mode='r') as file:
                data = json.load(file)
                self.email = data["email"]
                self.password = data["password"]
        except:
            print(
                "You are missing " + propertiesPath + ". Please ask Robert" \
                    "(robert.ciborowski@mail.utoronto.ca) for help.")


