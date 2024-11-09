import json
import os

output_file_path = os.path.join(os.path.dirname(__file__), "departmentLinks.txt")
departmentTags = os.path.join(os.path.dirname(__file__), "departmentTags.txt")

# Load your JSON data
with open(output_file_path, 'r') as file:
    data = file.readlines()  # Reads the file as a single string
    
tags = []
    
for url in data:
    tags.append(url.split('/')[-2].upper())
    
with open(departmentTags, 'w') as file:
    for tag in tags:
        file.write(tag + '\n')
    
print(tags)