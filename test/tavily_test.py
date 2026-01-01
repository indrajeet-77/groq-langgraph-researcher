from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Loading the environment variables
load_dotenv()

# creating a client instance of Tavily and passing the API key via dotenv
client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Here, 
# 1] Using the search method of that client instance that I have created.
# 2] Passes a desires query
# 3] Stored it into response
response=client.search(query="Name the 7 wonders of the world")

#  Printing the response
print(response)