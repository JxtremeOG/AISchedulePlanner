from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import random

# List of URLs to scrape
urlsOriginal = [
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=A',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=AS',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=B',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=CV',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=C',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=CI',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=E',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=PH',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=GC',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=X',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=NH',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=PE',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=R',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=T',
    'https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202445?collCode=L'
]

urls = [
]

# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # Use `webdriver.Firefox()` if you prefer Firefox

def extract_first_two_td_from_page(url, wait_time):
    driver.get(url)
    time.sleep(wait_time)  # Wait for JavaScript to load content
    
    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    extracted_data = []
    # Find all rows with class 'odd' or 'even'
    for row in soup.find_all("tr", class_=["odd", "even"]):
        tds = row.find_all("td")
        if len(tds) >= 2:  # Check if there are at least two <td> elements
            first_td = tds[0].get_text(strip=True)
            second_td = tds[1].get_text(strip=True)
            extracted_data.append((first_td, second_td))
    
    return extracted_data

def extractURLS(url, wait_time):
    driver.get(url)
    time.sleep(wait_time)  # Wait for JavaScript to load content
    
    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    urls = []  # List to store extracted URLs

    # Find all rows with class 'odd' or 'even'
    for row in soup.find_all(class_=["odd", "even"]):
        # Look for an <a> tag within the row and extract its URL if available
        link = row.find('a')
        if link and link.get('href'):
            urls.append(f"https://termmasterschedule.drexel.edu{link['href']}")

    return urls  # Return only the list of extracted URLs

output_file_path = os.path.join(os.path.dirname(__file__), "coursesFoundSummer.txt")
departFilePath = os.path.join(os.path.dirname(__file__), "coursesDepart.txt")

for index, url in enumerate(urlsOriginal):
    urls += [url]
    wait_time = 30 if index == 0 else 3
    print(f"Extracting data from {url} with a wait time of {wait_time} seconds")
    urls += extractURLS(url, wait_time)
    
# with open(departFilePath, "a") as file:
#     for index, url in enumerate(urls):
#         file.write(f"{url}\n")

# Iterate over each URL and extract data
with open(output_file_path, "a") as file:
    for index, url in enumerate(urls):
        wait_time = 3 if index == 0 else 3  # 30 seconds for the first URL, 3 seconds for the rest
        print(f"Extracting data from {url} with a wait time of {wait_time} seconds")
        
        data = extract_first_two_td_from_page(url, wait_time)
        
        for item in data:
            # Write each 'td1 td2' pair to the file, separated by a space
            print(f"{item[0]} {item[1]}")
            file.write(f"{item[0]} {item[1]}\n")

# Close the browser once done
driver.quit()
