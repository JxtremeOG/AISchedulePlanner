import json
import os

departmentTags = os.path.join(os.path.dirname(__file__), "departmentTags.txt")

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

# Load your JSON data
with open(departmentTags, 'r') as file:
    tags = file.readlines()
    
for tag in tags:
    # Remove any extra newline or whitespace from tag
    tag = tag.strip()
    
    # Path to each department's JSON file
    course_json_path = os.path.join(os.path.dirname(__file__), "courseJsons", f"{tag}.json")
    
    # Load the JSON data for each department
    with open(course_json_path, 'r') as file:
        data = json.load(file)

    # Add the "offered" field to each course
    for course in data:
        offeredTerms = ""
        if course["shortName"] in fallShortnames:
            offeredTerms += "Fall"
        if course["shortName"] in winterShortnames:
            offeredTerms += "Winter"
        if course["shortName"] in springShortnames:
            offeredTerms += "Spring"
        if course["shortName"] in summerShortnames:
            offeredTerms += "Summer"
        data[course]["offered"] = offeredTerms

    # Save the modified JSON back to the file
    with open(course_json_path, 'w') as file:
        json.dump(data, file, indent=4)

