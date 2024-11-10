import re
import json

class Course:
    
    def __init__(self, shortName="", fullName="", courseCredits=0.0, courseDesc="", courseDepartment="", 
                 repeatStatus="", prereqs="", coreqs="", restrictions="", offered=""):
        self.shortName = shortName
        self.fullName = fullName
        self.courseCredits = courseCredits
        self.courseDesc = courseDesc
        self.courseDepartment = courseDepartment
        self.repeatStatus = repeatStatus
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.restrictions = restrictions
        self.offered = offered
        
    def cleanPrerec(self):
        if self.prereqs != None:
            temp = re.sub(r'\[.*?\]', ' ', self.prereqs).strip()
            return re.sub(r'\s+', ' ', temp).strip().replace(" )", ")")
        return ""
        
    def toDict(self):
        return {
            'shortName': self.shortName,
            'fullName': self.fullName,
            'courseCredits': self.courseCredits,
            'courseDesc': self.courseDesc,
            'courseDepartment': self.courseDepartment,
            'repeatStatus': self.repeatStatus,
            'prereqs': self.prereqs,
            'coreqs' : self.coreqs,
            'restrictions' : self.restrictions,
            'offered' : self.offered,
        }
    
    ##Only return whats missing
    def getPrerecBranches(self):
        cleanPrerecs = self.cleanPrerec()
        splitBranches = [part.strip() for part in cleanPrerecs.split(' or ')]
        return splitBranches
        
        
    def __str__(self):
        return f"{self.shortName}\n{self.fullName}\nCredits: {self.courseCredits}\n{self.courseDesc}\n{self.courseDepartment}\nRepeat Status: {self.repeatStatus}\nPreequisites: {self.prereqs}\nCoequisites {self.coreqs}\nRestrictions: {self.restrictions}\nOffered: {self.offered}"
