from Course import Course
from Scheduler import Scheduler
import re

class PrereqNode:
    def __init__(self, value, schedule: Scheduler, isOperator=False):
        self.value = value  # Course name or operator ('and'/'or')
        self.isOperator = isOperator
        self.schedule = schedule
        self.term = schedule.findCourseTermIndex(value) if value not in ("and", "or") else -1
        self.children = []  # List of children nodes

    def addChild(self, node):
        self.children.append(node)
        
    def areChildrenValid(self):
        for child in self.children:
            if child is None:
                return True
            if child.getTerm() >= self.getTerm() or child.getTerm() == -1:
                return False
        return True
        
    def getTerm(self):
        # If the current node is an "or" operator, return the max term from its children
        if self.value == "or":
            termList = list(child.getTerm() for child in self.children)
            if all(element == -1 for element in termList):
                return -1
            if any(element == -1 for element in termList):
                return max(termList)
            return min(termList)

        # If the current node is an "and" operator, return the min term from its children
        if self.value == "and":
            termList = list(child.getTerm() for child in self.children)
            if any(element == -1 for element in termList):
                return -1
            return max(termList)

        return self.term
        
        
class PrereqTree:
    def __init__(self, courseGen: Course, schedule: Scheduler):
        self.root = PrereqNode(courseGen, schedule)
        self.nodeList = {}
        self.schedule = schedule
    
    def removeSurroundingParentheses(self, prereqStr):
        # Check if the string starts and ends with parentheses and contains valid content inside
        if prereqStr.startswith('(') and prereqStr.endswith(')'):
            # Use regular expression to check if there are nested parentheses
            # The pattern checks if the outer parentheses wrap the entire string without nested parentheses
            if re.match(r'^\([^()]*\)$', prereqStr):
                prereqStr = prereqStr[1:-1]  # Remove the outer parentheses if no nested parentheses exist
        return prereqStr
    
    def splitPrereqString(self, prereqStr):
        # First, apply parentheses removal to the whole string if needed
        prereqStr = prereqStr.replace(" (Can be taken Concurrently)", "")
        prereqStr = prereqStr.replace(",", " or")
        prereqStr = self.removeSurroundingParentheses(prereqStr).strip()
        
        # Regular expression to capture either a parenthesized group or a single course, followed by an operator, and the rest
        pattern = r'^(\(.*?\)|[A-Z]+\s\d+)\s+(and|or)\s+(.*)$'
        
        # Use search to match the first course (or parenthesized group), operator, and the rest of the string
        match = re.search(pattern, prereqStr)
        
        if match:
            # Split the string into the three parts
            first_part = match.group(1).strip()
            operator = match.group(2).strip()
            rest_of_string = match.group(3).strip()

            # Apply parentheses removal to each part
            first_part = self.removeSurroundingParentheses(first_part)
            rest_of_string = self.removeSurroundingParentheses(rest_of_string)
            
            return [first_part, operator, rest_of_string]
        else:
            # Handle cases where the pattern doesn't match (unlikely with the given format)
            return [prereqStr]
        
    def generateTree(self):
        self.root.addChild(self.extendTree(self.splitPrereqString(self.root.value.cleanPrerec())))
    
    def extendTree(self, prereqList: list):
        if len(prereqList) == 1 and len(prereqList[0]) > 0:  # Must be a course
            if "AP" in prereqList[0][0:2]:
                tempCourse = Scheduler.createCourseFromShortName("FAKE 000")
                self.schedule.addCourseToTerm(tempCourse, 0)
                node = PrereqNode(tempCourse, self.schedule)
                
            else:
                node = PrereqNode(Scheduler.createCourseFromShortName(prereqList[0]), self.schedule)
            # self.nodeList[node.value.shortName] = node
            if node.value.cleanPrerec() != "":
                node.addChild(self.extendTree(self.splitPrereqString(node.value.cleanPrerec())))
            return node
        elif len(prereqList[0]) == 0:
            return None
        else:
            node = PrereqNode(prereqList[1], self.schedule)  # This is an operator node ('and'/'or')
            node.isOperator = True

            # Recursively build the left and right children
            left_child = self.extendTree(self.splitPrereqString(prereqList[0]))
            right_child = self.extendTree(self.splitPrereqString(prereqList[2]))

            node.addChild(left_child)
            node.addChild(right_child)

            return node
    
    def printTree(self, parent: PrereqNode = None):
        if parent is None:
            parent = self.root

        # Print the course's short name if parent.value is a Course, else print the operator or value
        if isinstance(parent.value, Course):
            print(parent.value.shortName + " " + str(parent.getTerm()))
        else:
            print(parent.value + " " + str(parent.getTerm()))
        
        # Recursively print each child node
        for child in parent.children:
            if child is not None:
                self.printTree(child)
    
    def isValidNode(self, node: PrereqNode):
        if not node.isOperator:
            if node.term == -1:
                return False
            if len(node.children) == 0 or node.children[0] == None:
                return True
            childTerm = node.children[0].getTerm()
            if childTerm != -1 and node.term > childTerm:
                return self.isValidNode(node.children[0])
            return False
        if node.value == "or":
            return self.isValidNode(node.children[0]) or self.isValidNode(node.children[1])
        if node.value == "and":
            return self.isValidNode(node.children[0]) and self.isValidNode(node.children[1])
        
        
    
if __name__ == "__main__":
    #CS 342 MUST BE LOOKED AT
    #AP Classes will break
    #MATH 277 [WI] FIXED 
    
    mainSchedule = Scheduler()
    
    #CS 303 CS 281 CS 429
    #CS 375
    # createdCourse = Scheduler.createCourseFromShortName("CS 175")
    # mainSchedule.addCourseToTerm(createdCourse, 1)
    createdCourse = Scheduler.createCourseFromShortName("CS 270")
    mainSchedule.addCourseToTerm(createdCourse, 2)
    createdCourse = Scheduler.createCourseFromShortName("CS 260")
    mainSchedule.addCourseToTerm(createdCourse, 2)
    createdCourse = Scheduler.createCourseFromShortName("CS 380")
    mainSchedule.addCourseToTerm(createdCourse, 3)
    mainTree = PrereqTree(createdCourse, mainSchedule)
    mainTree.generateTree()
    
    print(mainTree.isValidNode(mainTree.root))
    
    # print("Tree:")
    # mainTree.printTree()
    
    