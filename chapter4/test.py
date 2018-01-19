from bs4 import BeautifulSoup
import urllib.request

def get(soup):
	v = soup.string
	if v == None:
		c = soup.contents
		resulttext = ''
		for t in c:
			subtext = get(t)
			resulttext += subtext + '\n'
		return resulttext
	else:
		return v.strip()
		
url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
a = urllib.request.urlopen(url)
html = a.read()
soup = BeautifulSoup(html, 'lxml')
print(get(soup))