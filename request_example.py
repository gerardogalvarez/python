'''' Example of use of requests'''
import requests

r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass_'), timeout=10)

print(r.status_code)
if r.ok:

    print(r.headers['content-type'])

    print(r.encoding)

    print(r.text)

    print(r.json())
else:
    print("Erro: ")
    print(f'{r.status_code} {r.reason}')
