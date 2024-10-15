import json
import os

# Define the directory where all the JSON files are stored
json_directory = 'courseJsons'  # Replace with the path to your JSON files
combined_data = {}

# Iterate over all files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):  # Check for JSON files
        file_path = os.path.join(json_directory, filename)

        # Open and load each JSON file
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                combined_data.update(data)  # Merge the data from each file
            except json.JSONDecodeError as e:
                print(f"Error parsing {filename}: {e}")

# Save the combined data into a new JSON file
output_file = 'masterJsons.json'
with open(output_file, 'w') as output_json_file:
    json.dump(combined_data, output_json_file, indent=4)

print(f"Combined JSON saved to {output_file}")
