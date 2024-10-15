from bs4 import BeautifulSoup
import requests
import re
import json

def map_text_in_outside_parentheses(text: str) -> dict:
    # Regular expression to find text inside and outside parentheses
    matches = re.findall(r'([^\(]+)\(([^)]+)\)', text)
    
    # Create a dictionary mapping outside text to inside text
    result = {inside.strip(): outside.strip() for outside, inside in matches}
    
    return result

url = 'https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

DepartmentColumns = soup.find_all(class_ = "qugcourses")

departDict = {}

for departmentColumn in DepartmentColumns:
    links = departmentColumn.find_all('a', href=True)
    for link in links:
        mapped_text = map_text_in_outside_parentheses(link.getText())
        
        departDict.update(mapped_text)
        
with open('department_mapping.json', 'w') as json_file:
    json.dump(departDict, json_file, indent=4)

