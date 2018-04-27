import sys

def main():
	size = 0
	puzzle = []
	words = []

	size = input()
	for i in range(size):
		line = raw_input()
		puzzle.append(line)

	for i in range(size):
		wa = ""
		wb = ""
		j = 0
		while j < size:
			if puzzle[i][j] != '#':
				wa += puzzle[i][j]
			else:
				if len(wa) > 1:
					words.append(wa)
				wa = ""
			if puzzle[j][i] != '#':
				wb += puzzle[j][i]
			else:
				if len(wb) > 1:
					words.append(wb)
				wb = ""

			j += 1
		if len(wa) > 1:
			words.append(wa)
		if len(wb) > 1:
			words.append(wb)

	for i in range(len(words)):
		sys.stdout.write(words[i])
		if(i != len(words)-1):
			sys.stdout.write(";")


if __name__ == '__main__':
	main()