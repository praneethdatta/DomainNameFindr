
from bs4 import BeautifulSoup
import requests
import re
url = 'http://getguru.com'
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')

for text in soup.stripped_strings:
    print text
    if u'\N{COPYRIGHT SIGN}' in text:
        #text = re.sub(r'\s+', ' ', text)  # condense any whitespace
        print(text)