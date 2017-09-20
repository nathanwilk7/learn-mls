from bs4 import BeautifulSoup
import pdb

html_doc = ''
html_path = 'audi-index'
with open(html_path, 'r') as r:
    for line in r:
        html_doc += line
pdb.set_trace()
soup = BeautifulSoup(html_doc, 'html.parser')

for link in soup.find_all('iframe'):
    print(link.get('src'))
