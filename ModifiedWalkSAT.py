import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice as SampleFromList
from numpy.random import random as RandomProbability
from tqdm import tqdm


def SatisfiesClause(Model, Clause):
	"""	Returns True if Model satisfies the Clause, else returns False
	"""
	LiteralList = np.array([int(Literal) for Literal in Clause[:-2].split()])
	return np.any([Literal * Model[abs(Literal)-1] > 0 for Literal in LiteralList])

def Satisfies(Model, ClauseList):
	""" Returns True if Model satisfies every clause in ClauseList, else returns False
	"""
	for Clause in ClauseList:
		if not SatisfiesClause(Model, Clause):
			return False
	return True

def FindVariablesInFalseClauses(Model, ClauseList):
	""" Returns a set of variables present in False-clauses in ClauseList
	"""
	VariablesInFalseClauses = set()
	for Clause in ClauseList:
		if not SatisfiesClause(Model, Clause):
			VariablesInFalseClauses.update([abs(int(Literal)) for Literal in Clause[:-2].split()])
	return np.array(list(VariablesInFalseClauses))

def FlipVariables(Model, FlippableVariables, NumVariablesToFlip):
	""" Randomly chooses a maximum of NumVariablesToFlip in FlippableVariables,
		flips their truth value in Model and returns modified Model
	"""
	NumVariablesToFlip = min(len(FlippableVariables), NumVariablesToFlip)
	VariablesToFlip = SampleFromList(FlippableVariables, size=NumVariablesToFlip, replace=False)
	for Variable in VariablesToFlip:
		Model[Variable - 1] *= -1
	return Model

def EvaluateFlip(VariableToFlip, Model, ClauseList):
	""" Helper function to rank the choice of variable to flip while taking maximum
	"""
	Model[VariableToFlip - 1] *= -1
	NumTrueClauses = np.sum([SatisfiesClause(Model, Clause) for Clause in ClauseList])
	Model[VariableToFlip - 1] *= -1
	return NumTrueClauses

def FlipMinConflictingVVars(Model, ClauseList, NumVariablesToFlip, NumVariables):
	""" Flips the truth values of a maximum of NumVariablesToFlip variables in Model,
		such that the total number of False-clauses are minimised,
		then returns the modified model
	"""
	Variables = set(range(1, NumVariables + 1))
	ClauseList_copy = set(ClauseList)
	for _ in range(NumVariablesToFlip):
		BestVariableToFlip = max(Variables, key=lambda x: EvaluateFlip(x, Model, ClauseList_copy))
		Model[BestVariableToFlip - 1] *= -1
		## < Dubious about this part >
		# Remove the clauses from ClauseList_copy that are satisfied by BestVariableToFlip
		ClausesToKeep = set(ClauseList_copy)
		for Clause in ClauseList_copy:
			if SatisfiesClause(Model, Clause):
				Model[BestVariableToFlip - 1] *= -1
				if not SatisfiesClause(Model, Clause):
					ClausesToKeep.remove(Clause)
		ClauseList_copy = ClausesToKeep
		## < Dubious about this part />
		Variables.remove(BestVariableToFlip)
	return Model

def ModifiedWalkSAT(C, p, maxit, maxv):
	""" Modified implementaion of WalkSAT algorithm that flips upto maxv variables at a time
	"""
	n, m = [int(x) for x in C[0][4:].split()]
	maxv = min(maxv, n)
	C = np.delete(C, 0)
	M = SampleFromList([+1, -1], size=n)
	v = 0
	t = 1
	while v <= maxv:
		v = v + 1
		while maxit > 0:
			maxit = maxit - 1
			if Satisfies(M, C):
				return (M, t)
			if RandomProbability() <= p:
				S = FindVariablesInFalseClauses(M, C)
				M = FlipVariables(M, S, v)
			else:
				M = FlipMinConflictingVVars(M, C, v, n)
			t += 1
	return (None, t)

def CreateCNF(k, m, n):
	""" Generates a k-CNF sentence with m clauses and n symbols, in DIMACS format
	"""
	CNF = ["cnf " + str(n) + " " + str(m)]
	# Generate a k-CNF problem with m clauses and n symbols
	ClauseList = set()
	SymbolsToChooseFrom = np.arange(1, n+1)
	while len(ClauseList) < m:
		# Get k literals without replacement
		LiteralsInThisClause = SampleFromList(SymbolsToChooseFrom, size=k, replace=False)
		LiteralsInThisClause = np.sort([str(x * -1) if RandomProbability() < 0.5 else str(x) for x in LiteralsInThisClause])
		ClauseList.add(" ".join(LiteralsInThisClause) + " 0")
	CNF +=  list(ClauseList)
	return np.array(CNF)

def TestModifiedWalkSAT():
	""" 
	"""
	NumTrials = 1
	k, p, maxit, maxv = 3, 0.5, 1000, 1
	Runtimes = dict()
	n = 50
	for r in tqdm(np.arange(1, 8, 1), desc="outer loop"):
		m = int(n * r)
		TotalRuntime = 0
		for i in tqdm(range(NumTrials), desc="inner loop", leave=False):
			TotalRuntime += ModifiedWalkSAT(CreateCNF(k, m, n), p, maxit, maxv)[1]
		Runtimes[m / n] = TotalRuntime / NumTrials
	plt.plot(*zip(*Runtimes.items()))
	plt.xticks(range(1, 11))
	plt.title("Performance Graph of ModifiedWalkSAT")
	plt.xlabel("m/n")
	plt.ylabel("Runtime (No. of assignments tried)")
	plt.show()

TestModifiedWalkSAT()
