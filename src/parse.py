import tatsu
import sys
from pathlib import Path
from ast import *

def error_exit(msg):
	print(msg)
	sys.exit()

def list_join(seq):
	return [seq[0]] + seq[1]

# -----------Semantic for TatSu parser to make an AST--------------------

class MySemantics(object):
	def fact(self, name):
		return Fact.get_fact(name)

	def Negation(self, ast):
		return NotExpr(ast)

	def And(self, ast):
		return AndExpr(list_join(ast))

	def Or(self, ast):
		return OrExpr(list_join(ast))

	def Xor(self, ast):
		return XorExpr(list_join(ast))

	def rule(self, ast):
		return Implies(ast[0], ast[2])

	def init(self, ast):
		return Init(ast)

	def query(self, ast):
		return Query(ast)

class ExpertParser():
	def __init__(self):
		Fact.init_fact_tree()
		try:
			self.path = str(Path(sys.argv[0]).parent) + '/'
			grammar = self.read_file('../syntax.peg')
			self.parser = tatsu.compile(grammar)
		except Exception:
			print("Don't touch syntax file!")
			sys.exit(1)

	def parse_str(self, query):
		return self.parser.parse(
			query + '\n',
			parseinfo=True,
			semantics=MySemantics(),
			trace=False,
			colorize=True,
			whitespace=''
		)

	def read_file(self, file):
		try:
			with open(self.path + file) as f:
				return "".join([line for line in f])
		except (FileNotFoundError, IsADirectoryError, PermissionError):
			print('Not a valid file')
			return None

	def parse_file(self, file):
		query = self.read_file(file)
		if query is None:
			return None
		elif query == "":
			return [[], [], []]
		else:
			result = self.parse_str(query)
			if result[0] == []:
				raise Exception("You missed rules!")
			if result[1] == []:
				raise Exception("You missed initial facts!")
			elif len(result[1]) > 1:
				raise Exception("You passed too much initial facts blocks!")
			if result[2] == []:
				raise Exception("You missed query!")
			elif len(result[2]) > 1:
				raise Exception("You passed too much query blocks!")
			return result
