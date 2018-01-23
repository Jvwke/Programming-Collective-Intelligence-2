import re
import math
import sqlite3

def sampletrain(cl):
	cl.train('Nobody owns the water.', 'good')
	cl.train('the quick rabbit jumps fences', 'good')
	cl.train('buy pharmaceuticals now', 'bad')
	cl.train('make quick money at the online casino', 'bad')
	cl.train('the quick brown fox jumps', 'good')
	
def getwords(doc):
	splitter = re.compile('\\W*')
	words = [s.lower() for s in splitter.split(doc) 
			if len(s)>2 and len(s)<20]
	return dict([(w,1) for w in words])
	
class classifier(object):
	def __init__(self, getfeatures, filename=None):
		self.fc = {}
		self.cc = {}
		self.getfeatures = getfeatures
	
	def incf(self, f, cat):
		count = self.fcount(f, cat)
		if count == 0:
			self.con.execute("insert into fc values ('%s', '%s', 1)"
								% (f, cat))
		else:
			self.con.execute(
				"update fc set count=%d where feature='%s' and category='%s'"
				%(count+1,f,cat))
	
	def incc(self, cat):
		count = self.catcount(cat)
		if count == 0:
			self.con.execute("insert into cc values ('%s', 1)" % (cat))
		else:
			self.con.execute("update cc set count=%d where category='%s'"
								% (count+1,cat))
	
	def fcount(self, f, cat):
		res = self.con.execute(
		'select count from fc where feature="%s" and category="%s"'
		% (f,cat)).fetchone()
		if res == None:
			return 0
		else:
			return float(res[0])
		
	def catcount(self, cat):
		res = self.con.execute('select count from cc where category="%s"'
							%(cat)).fetchone()
		if res == None:
			return 0
		else:
			return float(res[0])
		
	def totalcount(self):
		res = self.con.execute('select sum(count) from cc').fetchone()
		if res == None:
			return 0
		else:
			return res[0]
	
	def categories(self):
		cur = self.con.execute('select category from cc')
		return [d[0] for d in cur]
	
	def train(self, item, cat):
		features = self.getfeatures(item)
		for f in features:
			self.incf(f, cat)
		self.incc(cat)
		self.con.commit()
	
	def fprob(self, f, cat):
		if self.catcount(cat) == 0:
			return 0
		return self.fcount(f, cat)/self.catcount(cat)
		
	def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
		basciprob = prf(f, cat)
		totals = sum([self.fcount(f, c) for c in self.categories()])
		bp = ((weight*ap) + (totals*basciprob)) / (weight+totals)
		return bp
		
	def setdb(self, dbfile):
		self.con = sqlite3.connect(dbfile)
		self.con.execute('create table if not exists fc(feature,category,count)')
		self.con.execute('create table if not exists cc(category,count)')
	
		
class naviebayes(classifier):
	def __init__(self, getfeatures):
		classifier.__init__(self, getfeatures)
		self.thresholds = {}
		
	def setthreshold(self, cat, t):
		self.thresholds[cat] = t
		
	def getthreshold(self, cat):
		if cat not in self.thresholds:
			return 1.0
		return self.thresholds[cat]
		
	def classify(self, item, default=None):
		probs = {}
		max = 0.0
		for cat in self.categories():
			probs[cat] = self.prob(item, cat)
			if probs[cat] > max:
				max = probs[cat]
				best = cat
		for cat in probs:
			if cat==best:
				continue
			if probs[cat]*self.getthreshold(best) > probs[cat]:
				return default
		return best
		
	def docprob(self, item, cat):
		features = self.getfeatures(item)
		p = 1
		for f in features:
			p *= self.weightedprob(f, cat, self.fprob)
		return p
		
	def prob(self, item, cat):
		catprob = self.catcount(cat) / self.totalcount()
		docprob = self.docprob(item, cat)
		return catprob*docprob
	
class fisherclassifier(classifier):
	def __init__(self, getfeatures):
		classifier.__init__(self, getfeatures)
		self.minimums = {}

	def cprob(self, f, cat):
		clf = self.fprob(f, cat)
		if clf == 0:
			return 0
		freqsum = sum([self.fprob(f, c) for c in self.categories()])
		p = clf/(freqsum)
		return p
	
	def fisherprob(self, item, cat):
		p = 1
		features = self.getfeatures(item)
		for f in features:
			p *= (self.weightedprob(f, cat, self.cprob))
		fscore = -2*math.log(p)
		return self.invchi2(fscore, len(features)*2)
	
	def invchi2(self, chi, df):
		m = chi / 2.0
		sum = term = math.exp(-m)
		for i in range(1, df//2):
			term *= m/i
			sum += term
		return min(sum, 1.0)
		
	def setminimum(self, cat, min):
		self.minimums[cat] = min
	
	def getminimum(self, cat):
		if cat not in self.minimums:
			return 0
		return self.minimums[cat]
		
	def classify(self, item, default=None):
		max = 0.0
		best = default
		for c in self.categories():
			p = self.fisherprob(item, c)
			if p > self.getminimum(c) and p > max:
				best = c
				max = p
		return best
		
cl = fisherclassifier(getwords)
cl.setdb('test1.db')
sampletrain(cl)
cl2 = naviebayes(getwords)
cl2.setdb('test1.db')
print(cl2.classify('quick money'))
