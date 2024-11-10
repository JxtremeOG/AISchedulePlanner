import json
import os

fallFilePath = os.path.join(os.path.dirname(__file__), "coursesFoundFall.txt")
winterFilePath = os.path.join(os.path.dirname(__file__), "coursesFoundWinter.txt")
springFilePath = os.path.join(os.path.dirname(__file__), "coursesFoundSpring.txt")
summerFilePath = os.path.join(os.path.dirname(__file__), "coursesFoundSummer.txt")

# Load the short names from the file into a list for easier checking
with open(fallFilePath, 'r') as file:
    fallShortnames = {line.strip() for line in file}  # Use a set for faster lookup

with open(winterFilePath, 'r') as file:
    winterShortnames = {line.strip() for line in file}  # Use a set for faster lookup
    
with open(springFilePath, 'r') as file:
    springShortnames = {line.strip() for line in file}  # Use a set for faster lookup
    
with open(summerFilePath, 'r') as file:
    summerShortnames = {line.strip() for line in file}  # Use a set for faster lookup
    
masterPath = os.path.join(os.path.dirname(__file__), "..", "courseJsons", f"masterJsons.json")

# Load the JSON data for each department
with open(masterPath, 'r') as file:
    data = json.load(file)

# Add the "offered" field to each course
for course in data:
    offeredTerms = ""
    if data[course]["shortName"] in fallShortnames:
        offeredTerms += "Fall "
    if data[course]["shortName"] in winterShortnames:
        offeredTerms += "Winter "
    if data[course]["shortName"] in springShortnames:
        offeredTerms += "Spring "
    if data[course]["shortName"] in summerShortnames:
        offeredTerms += "Summer"
    data[course]["offered"] = offeredTerms

# Save the modified JSON back to the file
with open(masterPath, 'w') as file:
    json.dump(data, file, indent=4)

