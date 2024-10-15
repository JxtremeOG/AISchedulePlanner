from DrexelTerm import DrexelTerm
from Course import Course
import json
import os

#19 terms
class Scheduler():    
    
    with open('department_mapping.json', 'r') as json_file:
        departmentMappings = json.load(json_file)
    
    def __init__(self):
        self.termList = [DrexelTerm() for _ in range(19)]
        self.desiredClassList = []
        
    def findCourseTermIndex(self, currentCouse: Course):
        for term in range(len(self.termList)):
            if any(course.shortName == currentCouse.shortName for course in self.termList[term].courseList):
                return term
        return -1
        
    def checkValidCoursePlacement(self, checkCourse: Course, checkTerm: int):
        branch = checkCourse.getPrerecBranches()[0]
        
        
        if checkTerm>0 and branch!="":
            branchCourse = Scheduler.createCourseFromShortName(branch)[0]
            if any(course.shortName == branchCourse.shortName for course in self.termList[checkTerm-1].courseList):
                return self.checkValidCoursePlacement(branchCourse, checkTerm-1)        
            else:
                return self.checkValidCoursePlacement(checkCourse, checkTerm-1)      
        
        elif checkTerm<1 and branch!="":
            print("FALSE")
            return False
        else:
            print("True")
            return True
        
        
        
        # self.checkValidCoursePlacement(Scheduler.createCourseFromShortName(branch), checkTerm-1)
        
        
    def getCourseInfo(shortName: str):
        deperartment = Scheduler.departmentMappings[shortName.split(" ")[0]]
        # Open and load the JSON file
        with open(os.path.join('courseJsons', f'{deperartment}.json'), 'r') as json_file:
            courses = json.load(json_file)
        
        if shortName in courses:
            return courses[shortName]
        else:
            raise ValueError("No course found!")
        
    def createCourseFromShortName(shortName: str):
        courseInfo = Scheduler.getCourseInfo(shortName)
        newCourse = Course(courseInfo["shortName"], courseInfo["fullName"], courseInfo["courseCredits"], courseInfo["courseDesc"], courseInfo["courseDepartment"], courseInfo["repeatStatus"], courseInfo["prereqs"], courseInfo["coreqs"], courseInfo["restrictions"])
        return newCourse
        
        
if __name__ == "__main__":
    mainSchedule = Scheduler()
    
    #ADD 171
    createdCourse = Scheduler.createCourseFromShortName("CS 171")
    mainSchedule.termList[1].addCourse(createdCourse)
    
    createdCourse = Scheduler.createCourseFromShortName("CS 265")
    mainSchedule.termList[8].addCourse(createdCourse)
    
    createdCourse = Scheduler.createCourseFromShortName("CS 172")
    mainSchedule.termList[3].addCourse(createdCourse)
    
    mainSchedule.checkValidCoursePlacement(createdCourse, mainSchedule.findCourseTermIndex(createdCourse))
    
    
    