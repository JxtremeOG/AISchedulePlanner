from Course import Course

class DrexelTerm():
    
    def __init__(self):
        self.timeFrame = None
        self.currentCredits = 0.0
        self.coopTerm = False
        self.courseList = []
        
    def addCourse(self, addedCourse: Course):
        self.courseList.append(addedCourse)
        
    def removeCourse(self, removedCourse: Course):
        self.courseList.remove(removedCourse)
        
    def checkForCourse(self, checkCourse: Course):
        if checkCourse in self.courseList:
            return True
        return False