import requests

data = {
    'token': '0C2EBC92F7B66D7FBC3D6C0C4FE00E88',
    'content': 'record',
    'format': 'json',
    'returnFormat': 'json'
}

r = requests.post('https://redcap.icipe.org/api/', data)

print(r.text)

with open('records.json', 'w') as file:
    file.write(r.text)
