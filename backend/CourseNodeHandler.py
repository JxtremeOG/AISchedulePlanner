from Course import Course
import re

class CourseNode:
    def __init__(self, value: Course):
        self.value = value  #Course Object
        self.courseName = value.shortName
        self.term = -1
        self.preReqNodes = []
        self.status = "checkmark"
        
    def addNodeTerm(self, term):
        self.term = term
        
    def extractCourseNames(self, prereqString):
        # Use regex to find course names which are in the format "ABC 123"
        course_names = re.findall(r'[A-Z]{2,4} \d{3}', prereqString)
        return course_names