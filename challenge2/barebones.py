import sys, re

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
				kind = value  # classify as keyword
			elif kind == "whitespace":
				continue
			elif kind == "invalidChar":
				raise SyntaxError(f"Unexpected character {value!r}")

			tokens.append((kind, value.lower()))
		return tokens

class Parser():
	def __init__(self, tokens):
		self.tokens = tokens
		self.counter = 0
		self.expected = []
	
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
	
			self.counter += 1
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
				if self.symbolTable[self.astList[loopIndexes[-1]]["name"]] == 0:
					loopIndexes.pop()
				else:
					lineNum = loopIndexes[-1]
				if not loopIndexes:
					running = False
					continue
				# lineNum = loopIndexes[-1]
			
			lineNum += 1

		for symbol in self.symbolTable:
			print(f"{symbol}: {self.symbolTable[symbol]}", end = " | ")
		print("")






class Barebones():
	def __init__(self, filepath, silent = False):
		self.filepath = filepath
		self.silent = silent
		with open(self.filepath, "r") as f:
			self.code = f.read()

	def preprocess(self):
		if self.code[-1] != "\n":
			self.code += "\n"
		self.code = re.sub(r"#.*?\n", "", self.code)

	def interpret(self):
		self.preprocess()
		lexer = Lexer()
		tokens = lexer.tokenise(self.code)
		if len(tokens) > 0:
			parser = Parser(tokens)
			astList = parser.syntaxAnalysis()
			semanticAnalyser = SemanticAnalyser(astList)
			symbolTable = semanticAnalyser.semanticAnalysis()
			interpreter = Interpreter(astList, symbolTable)
			interpreter.interpret(silent=self.silent)

			# return (astList, symbolTable)



filepath = sys.argv[1]
# filepath = "testcode.bb"
barebones = Barebones(filepath)
barebones.interpret()
# astList, symbolTable = barebones.interpret()
# print(f"---AST list---\n{astList}\n\n---Symbol Table---\n{symbolTable}")