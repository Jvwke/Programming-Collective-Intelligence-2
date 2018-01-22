import random
import math

def printsolution(vec):
	slots = []
	for i in range(len(dorms)):
		slots += [i,i]
	for i in range(len(vec)):
		x = int(vec[i])
		dorm = dorms[slots[x]]
		print(prefs[i][0], dorm)
		del slots[x]

def dormcost(vec):
	cost = 0
	slots = [0,0,1,1,2,2,3,3,4,4]
	for i in range(len(vec)):
		x = int(vec[i])
		dorm = dorms[slots[x]]
		pref = prefs[i][1]
		if pref[0] == dorm:
			cost += 0
		elif pref[1] == dorm:
			cost += 1
		else:
			cost += 3
		del slots[x]
	return cost
	
def randomoptimize(domain, costf):
	best = 99999999
	bestr = None
	for i in range(1000):
		r = [random.randint(domain[i][0], domain[i][1])
			for i in range(len(domain))]
		print(r)
		cost = costf(r)
		if cost < best:
			best = cost
			bestr = r
	return r
	
def geneticoptimize(dmain, costf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100):
	def mutate(vec):
		i = random.randint(0, len(domain)-1)
		if random.random() < 0.5 and vec[i] > domain[i][0]:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		elif vec[i] < domain[i][1]:
			return vec[0:i]+[vec[i]+step]+vec[i+1:]
	def crossover(r1, r2):
		i = random.randint(1, len(domain)-2)
		return r1[0:i]+r2[i:]
	pop = []
	for i in range(popsize):
		vec = [random.randint(domain[i][0], domain[i][1])
				for i in range(len(domain))]
		pop.append(vec)
	topelite = int(elite*popsize)
	for i in range(maxiter):
		scores = [(costf(v), v) for v in pop]
		scores.sort()
		ranked = [v for (s,v) in scores]
		pop = ranked[0:topelite]
		while len(pop) < popsize:
			if random.random() < mutprob:
				c = random.randint(0, topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1 = random.randint(0, topelite)
				c2 = random.randint(0, topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))
		print(scores[0][0])
	return scores[0][1]
		
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']
prefs = [('Toby', ('Bacchus', 'Hercules')),
		('Steve', ('Zeus', 'Pluto')),
		('Andrea', ('Athena', 'Zeus')),
		('Sarch', ('Zeus', 'Pluto')),
		('Dave', ('Athena', 'Bacchus')),
		('Jeff', ('Hercules', 'Pluto')),
		('Fred', ('Pluto', 'Athena')),
		('Suzie', ('Bacchus', 'Hercules')),
		('Laura', ('Bacchus', 'Hercules')),
		('Neil', ('Hercules', 'Athena'))]
domain = [(0, (len(dorms)*2)-i-1) for i in range(0, len(dorms)*2)]
s = randomoptimize(domain, dormcost)
geneticoptimize(domain, dormcost)