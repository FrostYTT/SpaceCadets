# import modules
import sys

# define an interpreter class
class BareBones():
    def __init__(self):
        # get the filepath of the file from cli arguments
        self.programFilepath = sys.argv[1]
        print(self.programFilepath)
        self.lexer()
    
    # The lexer will preprocess and tokenise the code
    def lexer(self):
        # read all the lines of code
        with open(self.programFilepath, "r") as f:
            self.programLines = [line.strip() for line in f.readlines()]
        
        print(self.programLines)
        self.program = []
        self.tokenCounter = 0
        self.variables = {} # labelTracker = {}

        for line in self.programLines:
            parts = line.split(" ")
            



BareBones()

# program = []
# tokenCounter = 0
# labelTracker = {}

# for line in programLines:
#     parts = line.split(" ")
#     opcode = parts[0]
    
#     if opcode






# class Lexer():
#     def __init__(self):
#         pass

# class Parser():
#     def __init__(self):
#         pass

# class SemanticAnalyser():
#     def __init__(self):
#         pass

# class Interpreter():
#     def __init__(self):
#         pass

# class Main():
#     def __init__(self):
#         pass