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
        
    # def checkValidCoursePlacement(self, checkCourse: Course, checkTerm: int, branchNumber: int = 0, checkTermOriginal: int = 0):
    #     branch = checkCourse.getPrerecBranches()[branchNumber]
        
    #     if checkTerm>0 and branch!="":
    #         branchCourse = Scheduler.createCourseFromShortName(branch)
    #         if any(course.shortName == branchCourse.shortName for course in self.termList[checkTerm-1].courseList):
    #             return self.checkValidCoursePlacement(branchCourse, checkTerm-1, checkTermOriginal=checkTermOriginal)        
    #         else:
    #             return self.checkValidCoursePlacement(checkCourse, checkTerm-1,branchNumber=branchNumber, checkTermOriginal=checkTermOriginal)      
    #     elif checkTerm<1 and branch!="" and branch!=checkCourse.getPrerecBranches()[-1]:
    #         return self.checkValidCoursePlacement(checkCourse, checkTermOriginal, branchNumber+1, checkTermOriginal)
    #     elif checkTerm<1 and branch!="":
    #         print("FALSE")
    #         return False
    #     else:
    #         print("True")
    #         return True
        
    # def checkValidCoursePlacement(self, checkCourse: Course, checkTerm: int, branchNumber: int = 0, checkTermOriginal: int = 0):
        branch = checkCourse.getPrerecBranches()[branchNumber]
        courses = [part.strip() for part in branch.split(' and ')]
        for course in courses:
            # Base case: checkTerm is invalid and branch exists but we're not at the last branch
            if checkTerm < 1 and branch != "" and branch != checkCourse.getPrerecBranches()[-1]:
                return self.checkValidCoursePlacement(checkCourse, checkTermOriginal, branchNumber + 1, checkTermOriginal)
            # Base case: checkTerm is invalid, branch exists, and we're at the last branch
            if checkTerm < 1 and branch != "":
                # print("FALSE")
                return False
            # Base case: Branch is empty (meaning no prerequisites left) or checkTerm is valid
            if branch == "":
                # print("True")
                return True
            # Check if the prerequisite course is in the previous term's course list
            branchCourse = Scheduler.createCourseFromShortName(course)
            prevTermCourses = self.termList[checkTerm - 1].courseList
            if any(course.shortName == branchCourse.shortName for course in prevTermCourses):
                # Found the prerequisite course in the previous term, check further back
                return self.checkValidCoursePlacement(branchCourse, checkTerm - 1, checkTermOriginal=checkTermOriginal)
            # Recur with the same course but checking earlier terms
            return self.checkValidCoursePlacement(checkCourse, checkTerm - 1, branchNumber=branchNumber, checkTermOriginal=checkTermOriginal)
        
    def checkValidCoursePlacement(self, checkCourse: Course, checkTerm: int):
        branch = checkCourse.cleanPrerec()
        
        # Helper function to check if a course was taken in previous terms
        def isCourseTaken(courseReq, checkTerm):
            return any(
                course.shortName == Scheduler.createCourseFromShortName(courseReq).shortName
                for term in range(checkTerm, 0, -1)
                for course in self.termList[term - 1].courseList
            )
        
        # Process 'and' conditions
        courses = [part.strip() for part in branch.split(' and ')]
        if len(courses) > 1:  # AND condition
            return all(
                self.checkValidCoursePlacement(Scheduler.createCourseFromShortName(courseReq), checkTerm - 1) and
                isCourseTaken(courseReq, checkTerm)
                for courseReq in courses
            )
        
        # Process 'or' conditions
        if " or " in courses[0]:  # OR condition
            coursesOr = [part.strip("() ").strip() for part in courses[0].split(' or ')]
            return any(
                self.checkValidCoursePlacement(Scheduler.createCourseFromShortName(courseReq), checkTerm - 1) and
                isCourseTaken(courseReq, checkTerm)
                for courseReq in coursesOr
            )
        
        prereqCourse = courses[0].strip()
        
        if checkTerm < 1 and prereqCourse != "":
            return False
        
        if prereqCourse == "":
            return True
        
        # Check if the prerequisite course was completed in the previous term
        branchCourse = Scheduler.createCourseFromShortName(prereqCourse)
        prevTermCourses = self.termList[checkTerm - 1].courseList
        if any(course.shortName == branchCourse.shortName for course in prevTermCourses):
            # Recur for earlier terms if the course was found
            return self.checkValidCoursePlacement(branchCourse, checkTerm - 1)
        
        # Recur for the same course but checking earlier terms
        return self.checkValidCoursePlacement(checkCourse, checkTerm - 1)
        
    def checkCourseAndLogic(self, courses, checkTerm):
        return all(
                self.checkValidCoursePlacement(Scheduler.createCourseFromShortName(courseReq), checkTerm - 1) and
                any(
                    course.shortName == Scheduler.createCourseFromShortName(courseReq).shortName
                    for term in range(checkTerm, 0, -1)  # Loop through all previous terms
                    for course in self.termList[term - 1].courseList
                )
                for courseReq in courses
            )
        
    def checkCourseOrLogic(self, courses, checkTerm):
        coursesOr = [part.replace("(", "").replace(")", "").strip() for part in courses[0].split(' or ')]
        return any(
            self.checkValidCoursePlacement(Scheduler.createCourseFromShortName(courseReq), checkTerm - 1) and
            any(
                course.shortName == Scheduler.createCourseFromShortName(courseReq).shortName
                for term in range(checkTerm, 0, -1)  # Loop through all previous terms
                for course in self.termList[term - 1].courseList
            )
            for courseReq in coursesOr
        )
        
    def getCourseInfo(shortName: str):
        # Open and load the JSON file
        with open(os.path.join('courseJsons', f'{shortName.split(" ")[0]}.json'), 'r') as json_file:
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
    createdCourse = Scheduler.createCourseFromShortName("TEST 101")
    mainSchedule.termList[3].addCourse(createdCourse)
    
    createdCourse1 = Scheduler.createCourseFromShortName("TEST 100")
    mainSchedule.termList[0].addCourse(createdCourse1)
    
    createdCourse2 = Scheduler.createCourseFromShortName("TEST 99")
    mainSchedule.termList[0].addCourse(createdCourse2)
    
    createdCourse3 = Scheduler.createCourseFromShortName("TEST 102")
    mainSchedule.termList[4].addCourse(createdCourse3)
    
    createdCourse4 = Scheduler.createCourseFromShortName("TEST 103")
    mainSchedule.termList[6].addCourse(createdCourse4)
    
    # createCourseHURT = Scheduler.createCourseFromShortName("CS 281")
    # mainSchedule.termList[6].addCourse(createCourseHURT)
    # courses = [part.strip() for part in createCourseHURT.cleanPrerec().split(' and ')] #And separater
    # coursesOr = [part.replace("(", "").replace(")", "").strip() for part in courses[0].split(' or ')]  
    # print(coursesOr)
    # input()
    
    checkTerm = mainSchedule.findCourseTermIndex(createdCourse4)
    
    print(mainSchedule.checkValidCoursePlacement(createdCourse4, checkTerm))
    
    
    # def checkValidCoursePlacement(self, checkCourse: Course, checkTerm: int):
    #     checkCoursePrerecs = checkCourse.cleanPrerec()
        
        
        
        
        
    #     branch = checkCourse.cleanPrerec()
    #     courses = [part.strip() for part in branch.split(' and ')] #And separater
        
    #     if len(courses) > 1: #AND
    #         return self.checkCourseAndLogic(courses, checkTerm)
            
    #     if " or " in courses[0]: #OR
    #         return self.checkCourseOrLogic(courses, checkTerm)
        
    #     prereqCourse = courses[0]
        
    #     if checkTerm < 1 and prereqCourse != "":
    #         return False
        
    #     if prereqCourse == "":
    #         return True
    #     # Check if the prerequisite course is in the previous term's course list
    #     branchCourse = Scheduler.createCourseFromShortName(prereqCourse)
    #     prevTermCourses = self.termList[checkTerm - 1].courseList
    #     if any(course.shortName == branchCourse.shortName for course in prevTermCourses):
    #         # Found the prerequisite course in the previous term, check further back
    #         return self.checkValidCoursePlacement(branchCourse, checkTerm - 1)
    #     # Recur with the same course but checking earlier terms
    #     return self.checkValidCoursePlacement(checkCourse, checkTerm - 1)
    