from bs4 import BeautifulSoup
import requests

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Course import Course
import json
import os

class CourseScrape:
    
    def __init__(self, url):
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.CourseBlocks = self.soup.find_all(class_ = "courseblock")
        self.courseList = []
        
    def getCoursePage(self):
        self.soup.find(class_="page-title")
        return self.soup.find(class_="page-title").getText().strip()
    
    def writeToCourseFile(self):
        coursesData = {course.shortName: course.toDict() for course in self.courseList}
        with open(os.path.join('courseJsons', f'{self.courseList[0].shortName.split(" ")[0]}.json'), 'w') as json_file:
            json.dump(coursesData, json_file, indent=4)
            
    def scrapeWeirdNames(self):
        for courseBlock in self.CourseBlocks:
            currentCourse = Course()
            
            CourseBlockTitle = courseBlock.find(class_="courseblocktitle").find('strong')
            
            spans = CourseBlockTitle.find_all('span')

            currentCourse.shortName = spans[0].get_text(strip=True).replace('\u00a0', ' ')
            if '[' in currentCourse.shortName:
                print(currentCourse.shortName)
                
                
    def scrapeCourses(self):
        for courseBlock in self.CourseBlocks:
            print("Scraping...")
            currentCourse = Course()
            
            CourseBlockTitle = courseBlock.find(class_="courseblocktitle").find('strong')
            
            spans = CourseBlockTitle.find_all('span')

            currentCourse.shortName = spans[0].get_text(strip=True).replace('\u00a0', ' ')
            if '[WI]' in currentCourse.shortName:
                currentCourse.shortName = currentCourse.shortName.replace('[WI]', '').strip()
            
            currentCourse.fullName = spans[1].get_text(strip=True)
            # currentCourse.shortName = spans[2].get_text(strip=True) #Credits
            if len(spans) > 3:
                currentCourse.courseDesc = spans[3].get_text(strip=True)
            # The credit value (e.g., "3.0 Credits") isn't inside a span, so we get the remaining text
            currentCourse.courseCredits = CourseBlockTitle.find(string=True, recursive=False).strip()  # Only the text directly inside the strong tag
            currentCourse.courseDesc = courseBlock.find(class_="courseblockdesc").get_text(strip=True)
            
            # Now find the bold elements (<b>) with the specific text we want
            currentCourse.courseDepartment = courseBlock.find('b', string='College/Department:').next_sibling.strip()
            currentCourse.repeatStatus = courseBlock.find('b', string='Repeat Status:').next_sibling.strip()
            prereqsTag = courseBlock.find('b', string='Prerequisites:')
            restrictionsTag = courseBlock.find('b', string='Restrictions')
            coreqsTag = courseBlock.find('b', string='Corequisite')
            currentCourse.restrictions = restrictionsTag.next_sibling.strip().replace(":","").strip() if restrictionsTag else None
            currentCourse.prereqs = prereqsTag.next_sibling.strip().replace(":","").strip() if prereqsTag else None
            currentCourse.coreqs = coreqsTag.next_sibling.replace(":","").strip() if coreqsTag else None

            # print(currentCourse)
            # print()
            
            self.courseList.append(currentCourse)