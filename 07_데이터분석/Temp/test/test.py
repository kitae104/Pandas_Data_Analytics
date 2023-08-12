import requests
from bs4 import BeautifulSoup
req = requests.get("https://www.melon.com/chart/index.htm")
print(req)