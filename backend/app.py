# app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

from Course import Course
import CourseNodeHandler
from Scheduler import Scheduler
from PrerecHandler import PrereqTree

app = Flask(__name__)
socketio = SocketIO(app)
mainSchedule = Scheduler()

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/courseInfo', methods=['POST'])
def courseInfo():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    courseTerm = int(data.get('termNumber').split("-")[1])  # Extract the 'message' field from the JSON
    
    courseObject = Scheduler.createCourseFromShortName(courseShortName)
    
    #Update term in schedule
    oldTerm = mainSchedule.findCourseTermIndex(courseObject)
    if oldTerm != -1:
        mainSchedule.courses[courseShortName] = courseObject
        mainSchedule.removeCourseFromTerm(courseObject, oldTerm)
    mainSchedule.addCourseToTerm(courseObject, courseTerm-1)
    
    #Checking course validity
    preRecTree = PrereqTree(courseObject, mainSchedule)
    preRecTree.generateTree()
    courseValidity =  preRecTree.isValidMaxHeap()
    
    return jsonify({
        'validity': courseValidity
    })
    
@app.route('/courseStatus', methods=['POST'])
def getCourseStatus():
    data = request.get_json()  # This will retrieve the JSON sent by axios
    courseShortName = data.get('courseName')  # Extract the 'message' field from the 
    
    preRecTree = PrereqTree(Scheduler.createCourseFromShortName(courseShortName), mainSchedule)
    preRecTree.generateTree()
    courseValidity =  preRecTree.isValidMaxHeap()
    
    return jsonify({
        'validity': courseValidity
    })

if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)