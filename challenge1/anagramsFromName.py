# import modules
import requests

# set the path of the anagram files output ("" if in working directory)
path = "anagrams/"

# define a function to check if the name contains valid characters only
def alnumHyphenChecker(name):
    return all(character.isalnum() or character == '-' or character == " " for character in name)

# input the name from the user
name = str(input("Enter your name: "))
while not alnumHyphenChecker(name) or name == "":
    name = str(input("Invalid name, please try again: "))

# process the string to replace whitespace with + symbols for the url
name = name.replace(" ", "+").lower()
path += f"{name} anagram.txt"

# create the query url
url = f"https://new.wordsmith.org/anagram/anagram.cgi?anagram={name}"

# use requests to get web page data
response = requests.get(url)


# write HTML response to a file
with open(path, "w") as f:
    f.write(response.text)

# Read all lines from the file
with open(path, 'r') as file:
    lines = file.readlines()

# Initialize indices for the lines to keep
startIndex = 0
endIndex = len(lines)

# Find the line with the start_string
for i, line in enumerate(lines):
    if "found. Displaying all:" in line:
        startIndex = i + 1  # Start keeping lines after this one
        break

# Find the line with the end_string
for i in range(startIndex, len(lines)):
    if "<script>document.body.style.cursor='default';</script></div>" in lines[i]:
        endIndex = i  # Stop before this line
        break

# get sliced lines
sliced = lines[startIndex:endIndex]
# remove <br> tag from each line
for i in range(len(sliced)):
    sliced[i] = f"{sliced[i][:-5]}\n"
# process first and last lines
sliced[0] = sliced[0][8:]
sliced[len(sliced)-1] = sliced[len(sliced)-1][:-1]

# write lines to the file
with open(path, "w") as f:
    for line in sliced:
        f.write(line)