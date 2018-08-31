from parse import ExpertParser
from repl import ExpertSystem

counter = 0

def solve(file):
	solver = ExpertSystem()
	global counter
	counter += 1
	solver.parse_file(file)
	result = solver.get_solutions()
	print(counter, result)
	return result


def solve_tests():
	assert solve("../tests/INVALID_FOR_TESTS_1") == []
	assert solve("../tests/INVALID_FOR_TESTS_2") == []
	assert solve("../tests/OR_1") == ['False']
	assert solve("../tests/OR_2") == ['True']
	assert solve("../tests/OR_3") == ['True']
	assert solve("../tests/OR_4") == ['True']
	assert solve("../tests/FILE_NOT_PRESENT") == []
	assert solve("../tests/XOR_1") == ['False']
	assert solve("../tests/XOR_2") == ['True']
	assert solve("../tests/XOR_3") == ['True']
	assert solve("../tests/XOR_4") == ['False']
	assert solve("../tests/NEGATION_1") == ['False']
	assert solve("../tests/NEGATION_2") == ['True']
	assert solve("../tests/NEGATION_3") == ['False']
	assert solve("../tests/NEGATION_4") == ['False']
	assert solve("../tests/NEGATION_SIMPLE_1") == ['True']
	assert solve("../tests/NEGATION_SIMPLE_2") == ['False']
	assert solve("../tests/NEGATION_SIMPLE_3") == ['True']
	assert solve("../tests/MULTIPLE_RULES_1") == ['False']
	assert solve("../tests/MULTIPLE_RULES_2") == ['True']
	assert solve("../tests/MULTIPLE_RULES_3") == ['True']
	assert solve("../tests/MULTIPLE_RULES_4") == ['True']
	assert solve("../tests/STRANGE_OUTPUT_1") == []
	assert solve("../tests/STRANGE_OUTPUT_2") == []
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_1") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_2") == ['True']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_3") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_4") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_5") == ['True']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_6") == ['True']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_7") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_8") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_9") == ['False']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_10") == ['True']
	assert solve("../tests/PARENTHESISED_EXPRESSIONS_11") == ['True']
	assert solve("../tests/AND_1") == ['True', 'True', 'True', 'True']
	assert solve("../tests/AND_2") == ['True', 'True', 'False', 'True']
	assert solve("../tests/AND_LIST") == ['False']
	assert solve("../tests/AND_OR") == ['True']
	assert solve("../tests/BI_IF") == []
	assert solve("../tests/RIGHT_SIDE_OR") == ['Maybe(0.333)']
	print("Solve Test OK")


if __name__ == "__main__":
	solve_tests()
