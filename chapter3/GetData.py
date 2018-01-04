import feedparser
import re

def getwordcounts(url):
    d = feedparser.parse(url)
    wc = {}
    for e in d.entries:
        summary = e.description
        words = getwords(summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return d.feed.title, wc

def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word!='']

apcount = {}
wordcounts = {}
URL = open('URL.txt', 'r')
feedlist = [line for line in URL.readlines()]
print(feedlist)
for feedurl in feedlist:
	title, wc = getwordcounts(feedurl)
	wordcounts[title] = wc
	for word, count in wc.items():
		apcount.setdefault(word, 0)
		if count > 1:
			apcount[word] += 1
wordlist = []
for w, bc in apcount.items():
	frac = float(bc)/len(feedlist)
	if frac>0.1 and frac<0.8:
		wordlist.append(w)
out = open('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
	out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
	out.write(blog)
	for word in wordlist:
		if word in wc:
			out.write('\t%d' % wc[word])
		else:
			out.write('\t0')
	out.write('\n')
	print('Successfully')