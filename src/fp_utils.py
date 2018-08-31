
def head(seq):
	if seq != []:
		return seq[0]
	else:
		return []


def tail(seq):
	if len(seq) > 1:
		return seq[1:]
	else:
		return []


'''
	Split list or tuple on head and tail
	[0, 1, 2, 3, 4]   ->   0,   [1, 2, 3, 4]
	(	list		) -> (head)|(	tail	)
'''
def head_tail(seq):
	return head(seq), tail(seq)


''' Classic fold left '''
def fold(seq, acc, fn):
	if len(seq) == 0:
		return acc
	else:
		head, tail = head_tail(seq)
		return fold(tail, fn(acc, head), fn)
