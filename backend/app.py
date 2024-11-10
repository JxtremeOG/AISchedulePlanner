# app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
import logging

from Course import Course
import CourseNodeHandler
from Scheduler import Scheduler
from PrerecHandler import PrereqTree

app = Flask(__name__)
socketio = SocketIO(app)
mainSchedule = Scheduler()

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level of messages to log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    filename='app.log',  # Log file path
    filemode='w'  # Overwrite the file on each run, use 'a' to append
)

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/courseInfo', methods=['POST'])
def courseInfo():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    courseTerm = int(data.get('termNumber').split("-")[1])  # Extract the 'message' field from the JSON
    
    courseObject = Scheduler.createCourseFromShortName(courseShortName)
    logging.info("Created Course")
    
    #Update term in schedule
    oldTerm = mainSchedule.findCourseTermIndex(courseObject)
    if oldTerm != -1:
        mainSchedule.courses[courseShortName] = courseObject
        mainSchedule.removeCourseFromTerm(courseObject, oldTerm)
    mainSchedule.addCourseToTerm(courseObject, courseTerm)
    
    #Checking course validity
    preRecTree = PrereqTree(courseObject, mainSchedule)
    preRecTree.generateTree()
    courseValidity = preRecTree.isValidNode(preRecTree.root)
    
    return jsonify({
        'validity': courseValidity,
        'oldTerm': courseTerm
    })
    
@app.route('/courseStatus', methods=['POST'])
def getCourseStatus():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    
    preRecTree = PrereqTree(Scheduler.createCourseFromShortName(courseShortName), mainSchedule)
    preRecTree.generateTree()
    courseValidity =  preRecTree.isValidNode(preRecTree.root)
    
    
    return jsonify({
        'validity': courseValidity,
        'courseList': [course.shortName for course in mainSchedule.courses.values()]
    })
    
@app.route('/removeCourse', methods=['POST'])
def removeCourseFromSchedule():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    
    courseObject = Scheduler.createCourseFromShortName(courseShortName)
    oldTerm = mainSchedule.findCourseTermIndex(courseObject)
    mainSchedule.removeCourseFromTerm(courseObject, oldTerm)
    
    return jsonify({
        'validity': True
    })
    
@app.route('/courseDetails', methods=['POST'])
def getCourseDetails():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    
    courseObject = Scheduler.createCourseFromShortName(courseShortName)
    
    return jsonify({
        'courseInfo': courseObject.toDict()
    })
    
if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)