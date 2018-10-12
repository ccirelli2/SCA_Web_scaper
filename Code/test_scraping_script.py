
from bs4 import BeautifulSoup
from urllib.request import urlopen
Url = 'http://securities.stanford.edu/filings-case.html?id='

html = urlopen(Url + str(106750))
bsObj = BeautifulSoup(html.read(), 'lxml')
Tags = bsObj.find('section', {'id':'company'})
Defendant = Tags.find('h4')
print(Defendant.get_text().split(':')[1])

