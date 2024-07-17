from urllib.parse import quote
from urllib import request

while True:
    response = request.urlopen('http://127.0.0.1:8000/find/' + quote(input()))
    if response.status != 200:
        print('Err')
    else:
        print(*response)
