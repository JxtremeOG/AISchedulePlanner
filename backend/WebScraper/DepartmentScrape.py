from bs4 import BeautifulSoup
import requests

url = 'https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

DepartmentColumns = soup.find_all(class_ = "qugcourses")

for departmentColumn in DepartmentColumns:
    links = departmentColumn.find_all('a', href=True)
    for link in links:
        print("https://catalog.drexel.edu/" + link['href'])

