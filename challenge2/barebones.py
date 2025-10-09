#!/usr/bin/env python3
class Lexer():
	def __init__(self):
		self.validTokens = [
			('zero',      r'0'),
			('values',      r'\d+'),
			("identifier",  r"[A-Za-z_][A-Za-z0-9_]*"),
			("semicolon",   r";"),
			("whitespace",        r"[ \t]+"),
			("invalidChar",    r"."),
		]
		# Define reserved keywords
		self.reservedKeywords = ["clear", "incr", "decr", "copy", "to", "end", "while", "not", "do"]

	# Lexer function
	def tokenise(self, code):
		tokens = []
		tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.validTokens)
		# input(tok_regex)
		# input(re.finditer(tok_regex, code))

		for match in re.finditer(tok_regex, code):
			kind = match.lastgroup
			value = match.group()

			if kind == "identifier" and value in self.reservedKeywords:
				kind = value
			elif kind == "whitespace":
				continue
			elif kind == "invalidChar":
				raise SyntaxError(f"Unexpected character {value!r}")

			tokens.append((kind, value.lower()))
		return tokens

class Parser():
	def __init__(self, tokens, live = False):
		self.tokens = tokens
		self.counter = 0
		self.expected = []
		self.live = live
	
	def currentToken(self, adjust = 0):
		return self.tokens[self.counter + adjust]
	
	def addExpected(self, expected):
		for kind in expected:
			self.expected.append(kind)

	def aheadChecker(self, ahead, peekAmount, item):
		if ahead == peekAmount:
			raise SyntaxError(f"expected {item}")
		if self.currentToken(peekAmount+1)[0] != item:
			if item == "semicolon":
				raise SyntaxError(f"expected semicolon")
			raise SyntaxError(f"expected {item}, got {self.currentToken(peekAmount+1)[0]}")
	
	def checkerGrouper(self, amount, items):
		items = items.replace(" ", "").split(",")
		ahead = len(self.tokens) - self.counter - 1
		for i in range(amount):
			self.aheadChecker(ahead, i, items[i])

	def syntaxAnalysis(self):
		astList = []
		while self.counter < len(self.tokens):
			token = self.currentToken()

			if token[0] == "clear":
				self.checkerGrouper(2, "identifier,semicolon")
				astList.append({"type": "clear", "name": self.currentToken(1)[1]})
				self.counter += 2

			elif token[0] == "incr":
				self.checkerGrouper(2, "identifier,semicolon")
				astList.append({"type": "incr", "name": self.currentToken(1)[1]})
				self.counter += 2

			elif token[0] == "decr":
				self.checkerGrouper(2, "identifier,semicolon")
				astList.append({"type": "decr", "name": self.currentToken(1)[1]})
				self.counter += 2

			elif token[0] == "copy":
				self.checkerGrouper(4, "identifier,to,identifier,semicolon")
				astList.append({"type": "copy", "from": self.currentToken(1)[1], "to": self.currentToken(3)[1]})
				self.counter += 4
			
			elif token[0] == "while":
				self.checkerGrouper(5, "identifier,not,zero,do,semicolon")
				astList.append({"type": "while", "name": self.currentToken(1)[1]})

			elif token[0] == "end":
				self.checkerGrouper(1, "semicolon")
				astList.append({"type": "end"})
				self.counter += 1
			
			elif token[0] == "identifier":
				raise SyntaxError(f"Invalid syntax")
	
			self.counter += 1
		if not self.live:
			if astList[-1]["type"] != "end":
				raise SyntaxError(f"barebones code must end with 'end;'")
		return astList

class SemanticAnalyser():
	def __init__(self, astList):
		self.astList = astList
		self.symbolTable = {}

	def semanticAnalysis(self):
		for ast in self.astList:
			if ast["type"] == "clear" and ast["name"] not in self.symbolTable:
				self.symbolTable[ast["name"]] = 0
			elif ast["type"] in ["incr", "decr", "while"] and ast["name"] not in self.symbolTable:
				raise NameError(f"Variable '{ast["name"]}' not defined")
			elif ast["type"] == "copy":
				if ast["from"] not in self.symbolTable:
					raise NameError(f"Variable '{ast["from"]}' not defined")
				if ast["to"] not in self.symbolTable:
					raise NameError(f"Variable '{ast["to"]}' not defined")
		return self.symbolTable

class Interpreter():
	def __init__(self, astList, symbolTable):
		self.astList = astList
		self.symbolTable = symbolTable

	def interpret(self, silent = False):
		loopIndexes = []
		lineNum = 0
		running = True

		while running:
			if not silent:
				print(f"Line {lineNum}", end=" | ")
				for symbol in self.symbolTable:
					print(f"{symbol}: {self.symbolTable[symbol]}", end = " | ")
				print("")

			ast = self.astList[lineNum]
			
			if ast["type"] == "clear":
				self.symbolTable[ast["name"]] = 0
			elif ast["type"] == "incr":
				self.symbolTable[ast["name"]] += 1
			elif ast["type"] == "decr":
				self.symbolTable[ast["name"]] -= 1
				if self.symbolTable[ast["name"]] < 0:
					raise ArithmeticError(f"'{ast["name"]}' is -1. variables must be non-negative")
			elif ast["type"] == "copy":
				self.symbolTable[ast["to"]] = self.symbolTable[ast["from"]]
			elif ast["type"] == "while":
				loopIndexes.append(lineNum)
			elif ast["type"] == "end":
				if loopIndexes and self.symbolTable[self.astList[loopIndexes[-1]]["name"]] == 0:
					loopIndexes.pop()
				elif loopIndexes:
					lineNum = loopIndexes[-1]
				if not loopIndexes:
					running = False
					continue
				# lineNum = loopIndexes[-1]
			
			lineNum += 1

		print("END", end=" | ")
		for symbol in self.symbolTable:
			print(f"{symbol}: {self.symbolTable[symbol]}", end = " | ")
		print("")

class Barebones():
	def __init__(self, args):
		self.args = args

	def run(self):
		if args.targetfile:
			if not args.targetfile.endswith(".bb") and not args.targetfile.endswith(".txt"):
				print("Error: File must have a .bb or .txt extension.")
				sys.exit(1)
			try:
				self.interpretFromFile(args.targetfile, args.silent)
			except FileNotFoundError:
				raise FileNotFoundError(f"Couldn't find {args.targetfile} file")
		else:
			print("No file provided. Launching live interpreter")
			print("WELCOME MESSAGE")
			self.liveInterpreter(args.silent)

	def liveInterpreter(self, silent):
		pass


	def interpretFromFile(self, filepath, silent):
		# open file, read code
		with open(filepath, "r") as f:
			code = f.read()
		# preprocess code ( remove comments )
		if code[-1] != "\n":
			code += "\n"
		code = re.sub(r"#.*?\n", "", code)
		# lexical analysis
		lexer = Lexer()
		tokens = lexer.tokenise(code)
		# ensuring there is code in the program
		if len(tokens) > 0:
			# syntax analysis
			parser = Parser(tokens)
			astList = parser.syntaxAnalysis()
			# semantic analysis
			semanticAnalyser = SemanticAnalyser(astList)
			symbolTable = semanticAnalyser.semanticAnalysis()
			# interpretation
			interpreter = Interpreter(astList, symbolTable)
			interpreter.interpret(silent=silent)


if __name__ == "__main__":
	import sys, re, argparse
	argParser = argparse.ArgumentParser(description="Process a .bb or.txt, or launch the live interpreter.")
	argParser.add_argument("targetfile", nargs="?", default=None, help="Path to file")
	argParser.add_argument("-s", "--silent", action="store_true", help="Run in silent mode (variable output only at the end of the code)")
	args = argParser.parse_args()
	barebones = Barebones(args)
	barebones.run()