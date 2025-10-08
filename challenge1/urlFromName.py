# import modules
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# load API KEYS from the .env file
load_dotenv()
APITOKEN = os.getenv("APITOKEN")
CSETOKEN = os.getenv("CSETOKEN")

# input the name of the target
name = str(input("Enter name of target: "))
while name == "":
    name = str(input("No name entered. Please try again: "))

# query for google search
query = f"{name} site:https://www.ecs.soton.ac.uk/people/"

# define function for performing the google search
def googleSearch(query, apiToken, cseToken):
    try:
        # Initialize the Custom Search API client
        service = build("customsearch", "v1", developerKey=apiToken)
        
        # Execute the search
        result = service.cse().list(
            q=query,
            cx=cseToken,
            num=1
        ).execute()
        
        # Extract URLs from results
        urls = [item["link"] for item in result.get("items", [])]
        return urls
    
    except Exception as e:
        print(f"Error during google search: {e}")
        return []

# Run the search
results = googleSearch(query, APITOKEN, CSETOKEN)

# Ensure a link was found
if results != []:
    print(f"The url for {name} is {results[0]}")
else:
    print(f"Couldn't find the url for {name}.")