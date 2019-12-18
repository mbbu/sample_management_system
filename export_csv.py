import requests
import pandas as pd
from io import StringIO

data = {
    'token': '0C2EBC92F7B66D7FBC3D6C0C4FE00E88',
    'content': 'record',
    'format': 'csv',
    'returnFormat': 'csv'
}


r = requests.post('https://redcap.icipe.org/api/', data)
df = pd.read_csv(StringIO(r.text))
print(df)

with open('records.csv', 'w') as file:
    file.write(r.text)
