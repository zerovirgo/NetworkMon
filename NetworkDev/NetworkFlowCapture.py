import requests
from bs4 import BeautifulSoup
import re

def request1():
    url = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/'
    res = requests.get(url)
    res.text

request1()
link = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/chi2tpe_link120160322.html'
