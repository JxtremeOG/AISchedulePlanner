import os

output_file_path = os.path.join(os.path.dirname(__file__), "coursesFoundSummer.txt")

# Read the contents of your file
with open(output_file_path, 'r') as file:
    courses = file.readlines()

# Remove duplicates by converting to a set, then back to a sorted list
unique_courses = sorted(set(course.strip() for course in courses))

# Write the unique courses back to the file
with open(output_file_path, 'w') as file:
    for course in unique_courses:
        file.write(course + '\n')


