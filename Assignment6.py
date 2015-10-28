import getopt, sys

class Node:
	def __init__(self, name):
		self.name = name
		self.parents = None
		self.childrens = None
		self.values = None

# create network structure
def population():

	# creates nodes to use
	pollution = Node("Pollution")
	smoker = Node("Smoker")
	cancer = Node("Cancer")
	dyspnoea = Node("Dyspnoea")
	xRay = Node("X-ray")

	# add parents to nodes
	cancer.parents = {"s": smoker, "p": pollution}
	dyspnoea.parents = {"c": cancer}
	xRay.parents = {"c": cancer}

	# add childrens to nodes
	pollution.childrens = [cancer]
	smoker.childrens = [cancer]
	cancer.childrens = [xRay, dyspnoea]

	# add values to nodes
	# p = Low, ~p = High
	pollution.values = {
		"p": 0.9,
		"~p": 0.1
		}
	# "y" = True, "~y" = False
	smoker.values = {
		"s": 0.3,
		"~s": 0.7
		}
	cancer.values = {
		"c": {
			"~ps": 0.05,
			"~p~s": 0.02,
			"ps": 0.03,
			"p~s": 0.001
			},
		"~c": {
			"~ps": 0.95,
			"~p~s": 0.98,
			"ps": 0.97,
			"p~s": 0.999
			}
		}
	dyspnoea.values = {
		"d": {
			"c": 0.65,
			"~c": 0.3
			},
		"~d": {
			"c": 0.35,
			"~c": 0.7
			}
		}
	# x = pos, ~x = neg
	xRay.values = {
		"x": {
			"c": 0.9,
			"~c": 0.2
			},
		"~x": {
			"c": 0.1,
			"~c": 0.8
			}
		}
	return {
		"p": pollution,
		"s": smoker,
		"c": cancer,
		"d": dyspnoea,
		"x": xRay
		}
# setPrior func. change the probability for either s or p
def setPrior(graph, name, probability):
	graph[name.lower()].values[name.lower()] = probability
	graph[name.lower()].values["~" + name.lower()] = 1 - probability

def getProbability(node, evidince):
	print node.name
	# nodeRef is the first letter of the Node name
	nodeRef = (node.name[0]).lower()
	if(evidince.find(nodeRef) is not -1):
		if(evidince.find("~"+nodeRef) is -1):
			return 1
		else:
			return 0
	else:
		if(node.parents is None):
			return node.values[nodeRef]
		else:
			negating = False
			probability = 0
			#i = node.values[(node.name[0]).lower()] which means the key inside of
			# nodeRef.
			for i in ((node.values[nodeRef]).keys()):
				#if(not isinstance(i, float)):
				x = (node.values[nodeRef])[i]
				print i, "With probability", x
				levelProbability = 1
				parentProbability = None
				for j in i:
					# if the current j is for example ~p we want to know p is negated
					# so we acknowlodge that and continue
					if(j[0] is "~"):
						negating = True
						continue
					else:
						nodeParent = node.parents[j[0]]
					parentProbability = getProbability(nodeParent, evidince)
					# for example if we have ~p then our probability = 1-p
					if(negating):
						negating = False
						parentProbability = 1 - parentProbability
					# we have to multibly levelProbability to each other
					levelProbability *= parentProbability
					print "parent =", parentProbability, "level =", levelProbability
				# x is the probability of the node
				probability += x * levelProbability
			return probability

def calcConditional(graph, name, givens):
	nameFirstLetter = name[len(name)-1].lower()
	probability = getProbability(graph[nameFirstLetter], givens)
	if(name[0] is "~"):
		return 1 - probability
	else:
		return probability
		
def printCapital (graph, name, probability):
	if(name == name.lower()):
		print name, "is", probability
	else:
		if(name[0] == "~"):
			print name[len(name)-1], "is", 1 - probability
			print name, "is", probability
		else:
			print name, "is", probability
			print "~"+name, "is", 1 - probability

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	# to create the graph.
	graph = population()
	for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			print "Before change prior:", graph[a[0].lower()].values[a[0].lower()]
			#setting the prior here works if the Bayes net is already built
			setPrior(graph, a[0], float(a[1:]))
			print "After change prior:", graph[a[0].lower()].values[a[0].lower()]

		elif o in ("-m"):
			print "flag", o
			print "args", a
			print type(a)
			print "Marginal is: ", calcConditional(graph, a, "")
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print a[:p]
			print a[p+1:]
			print calcConditional(graph, a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
		else:
			assert False, "unhandled option"

	# ...

if __name__ == "__main__":
	main()
