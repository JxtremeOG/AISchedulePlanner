from CourseScrape import CourseScrape


departmentLinksList = []

with open(r'C:\Users\zoldw\Projects\Coding\AISchedulePlanner\backend\WebScraper\departmentLinks.txt', 'r') as file:
    for line in file:
        departmentLinksList.append(line.strip())

for link in departmentLinksList:
    scraper = CourseScrape(link)
    scraper.scrapeCourses()
    scraper.writeToCourseFile()
    # scraper.scrapeWeirdNames()
    