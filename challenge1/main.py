# import modules
import requests, re, ast

# create a function for fetching the name of the target from an ID
def fetchName(url):
    # use the requests module to get a response from the url
    response = requests.get(url)

    # Check for HTTP errors
    if response.status_code == 200:
        # code 200 = OK
        # response.text contains a bit of code where the name of the target is given in the following json format: "name": "name of target"
        # the name can be searched for with this standard format using re module (re.findall)
        names = re.findall('"name": ".*"', response.text)

        # ensure some names have been returned, otherwise print error message
        if len(names) > 0:
            # names found
            # names is an array of two strings, 1st is irrelevant. Turning 2nd string into a python dictionary to fetch the name
            name = ast.literal_eval("{" + names[1] + "}")["name"]
            return f"The name of the target is: {name}"
        else:
            # no names found
            return "Failed to find target"
    elif response.status_code == 404:
        # 404 error
        return "Failed to reach website."
    else:
        # unknown error
        return f"Error. Status code: {response.status_code}"



# get the email ID from the user
id = str(input("Enter the email ID of the target: "))
while id == "":
    id = str(input("No ID entered. Please try again: "))

# concat email ID with the url of the website
url = "https://www.ecs.soton.ac.uk/people/" + id


print(fetchName(url))