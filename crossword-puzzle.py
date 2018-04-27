import sys
import time

size = 0
puzzle = [[]]
vCell = []
hCell = []
words = []
wordTaken = []

def user_input():
	global puzzle, words, size, wordTaken

	filename = raw_input("Filename: ")
	file = open(filename, "r+")

	size = int(file.read(3))

	for c in range(size+1):
		words.append([])
		wordTaken.append([])

	puzzle = [['-' for i in xrange(size)] for i in xrange(size) ]
	for row in range(size):
		strRow = file.read(size+1)
		strRow = strRow[0:size]
		for c in range(size):
			if strRow[c] == '#':
				puzzle[row][c] = '#'

	raw_words = file.read().split(";")
	for c in range(len(raw_words)):
		words[len(raw_words[c])].append(raw_words[c])
		wordTaken[len(raw_words[c])].append(False)

def observe_input():
	global puzzle, vCell, hCell, size

	evRow = -1
	evCol = [-1 for i in xrange(size)]

	for row in range(size):
		for col in range(size):
			if puzzle[row][col] == '-':
				if evRow == -1:
					evRow = col
				if evCol[col] == -1:
					evCol[col] = row
			else:
				if evRow != -1:
					if (col-1-evRow) > 0:
						hCell.append([evRow, col-1, row])
					evRow = -1
				if evCol[col] != -1:
					if (row-1-evCol[col]) > 0:
						vCell.append([evCol[col], row-1, col])
					evCol[col] = -1
			if row == (size-1) and evCol[col] != -1 and (row-evCol[col]) > 0:
				vCell.append([evCol[col], row, col])
		if evRow != -1:
			if (col-evRow) > 0:
				hCell.append([evRow, col, row])
			evRow = -1

	for i in range(len(vCell)):
		pos = i
		for j in range(i+1, len(vCell)):
			if vCell[j][0] < vCell[pos][0]:
				pos = j
			elif vCell[j][0] == vCell[pos][0] and vCell[j][2] > vCell[pos][2]:
				pos = j
		if pos != i:
			vCell[i], vCell[pos] = vCell[pos], vCell[i]

def solveHorizontal(hIterator, vIterator, level):
	global puzzle, hCell, words, wordTaken

	if hIterator >= len(hCell) or hCell[hIterator][2] != level:
		if level+1 == size:
			return True
		else:
			return solveVertical(hIterator, vIterator, level)

	segmentLen = hCell[hIterator][1] - hCell[hIterator][0] + 1
	row = hCell[hIterator][2]
	col = hCell[hIterator][0]
	currentSegment = puzzle[row][col:col+segmentLen]

	found = False
	wordIndex = 0
	while not found and wordIndex < len(words[segmentLen]):
		if not wordTaken[segmentLen][wordIndex]:
			i = 0
			while i < segmentLen and (currentSegment[i] == words[segmentLen][wordIndex][i] or currentSegment[i] == '-'):
				i += 1

			if i == segmentLen:
				i = 0
				while (i + col) < (col + segmentLen):
					puzzle[row][i + col] = words[segmentLen][wordIndex][i]
					i += 1
				wordTaken[segmentLen][wordIndex] = True

				found = solveHorizontal(hIterator+1, vIterator, level)

				if not found:
					wordTaken[segmentLen][wordIndex] = False
					i = 0
					while (i + col) < (col + segmentLen):
						puzzle[row][i + col] = currentSegment[i]
						i += 1

		wordIndex += 1

	return found

def solveVertical(hIterator, vIterator, level):
	global puzzle, vCell, words, wordTaken

	if vIterator >= len(vCell) or vCell[vIterator][0] != level:
		return solveHorizontal(hIterator, vIterator, level+1)

	segmentLen = vCell[vIterator][1] - vCell[vIterator][0] + 1
	col = vCell[vIterator][2]
	row = vCell[vIterator][0]
	currentSegment = ''
	for j in range(row, row + segmentLen):
		currentSegment = currentSegment + puzzle[j][col]

	found = False
	wordIndex = 0
	while not found and wordIndex < len(words[segmentLen]):
		if not wordTaken[segmentLen][wordIndex]:
			i = 0
			while i < segmentLen and (currentSegment[i] == words[segmentLen][wordIndex][i] or currentSegment[i] == '-'):
				i += 1

			if i == segmentLen:
				i = 0
				while (i + row) < (row + segmentLen):
					puzzle[i + row][col] = words[segmentLen][wordIndex][i]
					i += 1
				wordTaken[segmentLen][wordIndex] = True

				found = solveVertical(hIterator, vIterator+1, level) 

				if not found:
					wordTaken[segmentLen][wordIndex] = False
					i = 0
					while (i + row) < (row + segmentLen):
						puzzle[i + row][col] = currentSegment[i]
						i += 1

		wordIndex += 1

	return found

def print_puzzle():
	global puzzle, size

	for row in range(size):
		for col in range(size):
			sys.stdout.write(puzzle[row][col])		
		print('')

def main():
	user_input()
	observe_input()

	print('')
	timeBefore = time.time()
	if solveHorizontal(0, 0, 0):
		timeAfter = time.time()
		print "SOLVED! I need", (timeAfter - timeBefore), "seconds to solve it."
		print_puzzle()
	else:
		print "I CAN'T SOLVE IT!"

if __name__ == '__main__':
    main()