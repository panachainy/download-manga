import urllib.request
url = 'https://www.python.org/static/apple-touch-icon-144x144-precomposed.png'

headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response, open('filename2.jpg', 'wb') as outfile:
    outfile.write(response.read())
