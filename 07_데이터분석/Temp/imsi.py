import pyodide_http
import base64
from bs4 import BeautifulSoup

pyodide_http.patch_all()  # Patch all libraries

import requests

# data = requests.get("http://127.0.0.1:5500/HTTP/test.md")
# data = requests.get("http://127.0.0.1:5500/HTTP/passby_data.csv")
data = requests.get("http://127.0.0.1:5500/pyodide_app/HTTP/pyscript.html")

html = data.text
soup = BeautifulSoup(html, 'html.parser')
# ul = soup.select_one('#image-wrapper')
print(soup)