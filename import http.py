"""documentación mínima"""
import http.client as c

conn = c.HTTPSConnection("www.africau.edu")
payload = ''
headers = {}
conn.request("GET", "/images/default/sample.pdf", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))