from Scheduler import Scheduler
import CourseNodeHandler
from PrerecHandler import PrereqTree


if __name__ == "__main__":
    mainSchedule = Scheduler()
    courseShortName2 = "CS 171"
    mainSchedule.addCourseToTerm(Scheduler.createCourseFromShortName(courseShortName2), 1)
    courseShortName2 = "CS 172"
    mainSchedule.addCourseToTerm(Scheduler.createCourseFromShortName(courseShortName2), 2)
    courseShortName = "CS 265"
    mainSchedule.addCourseToTerm(Scheduler.createCourseFromShortName(courseShortName), 3)
    # courseShortName = "CS 175"
    # mainSchedule.addCourseToTerm(Scheduler.createCourseFromShortName(courseShortName), 1)
    preRecTree = PrereqTree(Scheduler.createCourseFromShortName(courseShortName), mainSchedule)
    preRecTree.generateTree()
    courseValidity =  preRecTree.isValidMaxHeap()
    print(courseValidity)