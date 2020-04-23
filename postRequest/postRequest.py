import requests


class postRequest:
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

