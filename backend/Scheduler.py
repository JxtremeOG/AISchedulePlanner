from DrexelTerm import DrexelTerm
from Course import Course
import CourseNodeHandler
import json
import os
import re

#19 terms
class Scheduler():    
    
    with open('department_mapping.json', 'r') as json_file:
        departmentMappings = json.load(json_file)
    
    def __init__(self):
        self.termList = [DrexelTerm() for _ in range(19)]
        self.desiredClassList = []
        self.courses = {}
        
    def findCourseTermIndex(self, currentCouse: Course):
        for term in range(len(self.termList)):
            if any(course.shortName == currentCouse.shortName for course in self.termList[term].courseList):
                return term
        return -1
        
    def addCourseToTerm(self, course: Course, term: int):
        self.termList[term].addCourse(course)
            
    def removeCourseFromTerm(self, courseCurrent: Course, term: int):
        for course in self.termList[term].courseList:
            if course.shortName == courseCurrent.shortName:
                self.termList[term].removeCourse(course)
        
    def getCourseInfo(shortName: str):
        # Open and load the JSON file
        with open(os.path.join('courseJsons', f'{shortName.split(" ")[0]}.json'), 'r') as json_file:
            courses = json.load(json_file)
        
        if shortName in courses:
            return courses[shortName]
        else:
            with open(os.path.join('courseJsons', f'{"FAKE"}.json'), 'r') as json_file:
                courses = json.load(json_file)
            return courses["FAKE 001"]
        
    def createCourseFromShortName(shortName: str):
        courseInfo = Scheduler.getCourseInfo(shortName)
        newCourse = Course(courseInfo["shortName"], courseInfo["fullName"], courseInfo["courseCredits"], courseInfo["courseDesc"], courseInfo["courseDepartment"], courseInfo["repeatStatus"], courseInfo["prereqs"], courseInfo["coreqs"], courseInfo["restrictions"], courseInfo["offered"])
        return newCourse
        
    
    
    