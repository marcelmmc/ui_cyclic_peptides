
class Paper:
   def __init__(self, title, url, year, authors, isOpenAccess,paperId):
      self.paperId = paperId
      self.title = title
      self.url = url 
      self.year = year 
      self.authors = authors
      self.isOpenAcess = isOpenAccess
    
   def __str__(self) -> str:
       return f'''
       title: {self.title}
       nurl: {self.url}
       year: {self.year}
       authors: {[name['name'] for name in self.authors]}
       OpenAcess: {'Yes' if self.isOpenAcess else 'No'}\n'''
   
import requests
# Define the API endpoint URL

paper = '10.1021/acs.jmedchem.0c00013'
url = f'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/doi:{paper}'

# More specific query parameter
# query_params = {'query': 'doi:10.1021/acs.jmedchem.0c00013'}
query_params = {'fields': 'title,url,year,authors,isOpenAccess', 'limit': '4'}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
api_key = ''  # Replace with the actual API key

# Define headers with API key
headers = {'x-api-key': api_key}


# Send the API request
response = requests.get(url, params=query_params, headers=headers)
print('response:',response)
# Check response status
if response.status_code == 200:
   response_data = response.json()
   # Process and print the response data as needed
   for paper in  response_data['recommendedPapers']:
      paper = Paper(**paper)
      print(paper)
else:
   print(f"Request failed with status code {response.status_code}: {response.text}")