import matplotlib.pyplot as plt
from random import random as RandomProbability
from random import choices as SampleWithReplacement
from random import sample as SampleWithoutReplacement

def SatisfiesClause(Model, Clause):
	"""	Returns True if Model satisfies the Clause, else returns False """
	LiteralList = [int(Literal) for Literal in Clause[:-2].split()]
	return any([Literal * Model[abs(Literal)-1] > 0 for Literal in LiteralList])

def Satisfies(Model, ClauseList):
	""" Returns True if Model satisfies every clasue in ClauseList, else returns False """
	for Clause in ClauseList:
		if not SatisfiesClause(Model, Clause):
			return False
	return True

def FindVariablesInFalseClauses(Model, ClauseList):
	""" Returns a set of variables present in False-clauses in ClauseList """
	VariablesInFalseClauses = set()
	for Clause in ClauseList:
		if not SatisfiesClause(Model, Clause):
			VariablesInFalseClauses.update([abs(int(Literal)) for Literal in Clause[:-2].split()])
	return VariablesInFalseClauses

def FlipVariables(Model, FlipableVariables, NumVariablesToFlip):
	""" Randomly chooses a maximum of NumVariablesToFlip in FlipableVariables,
		flips their truth value in Model and returns modified Model
	"""
	NumVariablesToFlip = min(len(FlipableVariables), NumVariablesToFlip)
	VariablesToFlip = SampleWithoutReplacement(FlipableVariables, NumVariablesToFlip)
	for Variable in VariablesToFlip:
		Model[Variable - 1] *= -1
	return Model

def EvaluateFlip(VariableToFlip, Model, ClauseList):
	Model[VariableToFlip - 1] *= -1
	NumTrueClauses = sum([SatisfiesClause(Model, Clause) for Clause in ClauseList])
	Model[VariableToFlip - 1] *= -1
	return NumTrueClauses

def FlipMinConflictingVVars(Model, ClauseList, NumVariablesToFlip, NumVariables):
	""" Flips the truth values of a maximum of NumVariablesToFlip variables in Model,
		such that the total number of False-clauses are minimised,
		then returns the modified model
	"""
	Variables = set(range(1, NumVariables + 1))
	for _ in range(NumVariablesToFlip):
		BestVariableToFlip = max(Variables, key=lambda x: EvaluateFlip(x, Model, ClauseList))
		Model[BestVariableToFlip - 1] *= -1
		Variables.remove(BestVariableToFlip)
	return Model

def ModifiedWalkSAT(C, p, maxit, maxv):
	""" Modified implementaion of WalkSAT algorithm that flips upto maxv variables at a time """
	n, m = [int(x) for x in C[0][4:].split()]
	maxv = min(maxv, n)
	del C[0]
	M = SampleWithReplacement([+1, -1], k=n)
	v = 0
	t = 1
	while v <= maxv:
		v = v + 1
		while maxit > 0:
			maxit = maxit - 1
			if Satisfies(M, C):
				return (M, t)
			S = FindVariablesInFalseClauses(M, C)
			print(S)
			if RandomProbability() <= p:
				M = FlipVariables(M, S, v)
			else:
				M = FlipMinConflictingVVars(M, C, v, n)
			t += 1
	return (None, t)

# print(ModifiedWalkSAT(["cnf 3 4", "3 -2 1 0", "-3 2 -1 0", "-2 -1 3 0", "1 2 -3 0"], 0.1, 10, 1))

def CreateCNF(k, m, n):
	CNF = ["cnf " + str(n) + " " + str(m)]
	for _ in range(m):
		

def TestWalkSAT():
	""" """
	NumTrials = 100
	k = 5
	for _ in NumTrials:
		for m in range(1, 101):
			for n in range(1, 11):
				for _ in range(50):
					# Create a k-CNF(m, n) a problem
					Problem = CreateCNF(k, m, n)


print(CreateCNF(3, 3, 4))
