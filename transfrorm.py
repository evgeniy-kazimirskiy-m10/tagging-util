import os
import re

# Directory containing the .feature files
directory_path = 'C:\\Users\\abade\\IdeaProjects\\pasha\\backend-integration-tests\\backend-tests\\src\\test\\resources\\features'
# Path to the failed tests file
failed_tests_file_path = './failed_tests.txt'
# Tag to add
tag = '@failed'

# Read the list of failed test cases
with open(failed_tests_file_path, 'r', encoding='utf-8') as failed_tests_file:
  failed_tests = [line.strip() for line in failed_tests_file]

# Function to check if a scenario contains any failed test case
def scenario_contains_failed(scenario_name):
  return any(scenario_name in failed_test for failed_test in failed_tests)

# Function to add a tag to matching scenarios if the tag does not already exist
def tag_failed_scenarios(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

  # Store the modified content here
  modified_content = []
  scenario_block = []  # Temporary buffer to store each scenario block
  in_scenario = False  # Flag to track if we're inside a scenario
  scenario_name = None
  already_tagged = False  # Flag to check if the scenario is already tagged

  for line in content:
    # Match scenario or scenario outline
    scenario_match = re.match(r'^\s*(Структура сценария|Scenario|Scenario Outline):\s*(.*)', line)
    if scenario_match:
      # If a new scenario starts, process the previous one
      if scenario_block and scenario_contains_failed(scenario_name) and not already_tagged:
        modified_content.append(f'{tag}\n')  # Add tag before the scenario block
      modified_content.extend(scenario_block)

      # Start a new scenario
      scenario_block = [line]  # Initialize scenario block with the first line
      scenario_name = scenario_match.group(2).strip()  # Capture the scenario name
      already_tagged = False  # Reset the tag flag for the new scenario
      in_scenario = True
    elif in_scenario:
      # Check if the tag already exists in the scenario block
      if tag in line:
        already_tagged = True

      # Collect lines inside the current scenario
      scenario_block.append(line)
      # End of scenario, add block to the content
      if line.strip().startswith('@allure.id') or line.strip() == '':
        in_scenario = False
        # If this scenario contains a failed test case and is not already tagged, add the tag
        if scenario_name and scenario_contains_failed(scenario_name) and not already_tagged:
          modified_content.append(f'{tag}\n')
        modified_content.extend(scenario_block)
        scenario_block = []

    else:
      # Outside any scenario, append the line normally
      modified_content.append(line)

  # Write the modified content back to the file
  with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(modified_content)

# Recursively find and modify all .feature files in the directory
for root, dirs, files in os.walk(directory_path):
  for file in files:
    if file.endswith('.feature'):
      print(f"Processing {file}...")
      file_path = os.path.join(root, file)
      tag_failed_scenarios(file_path)

print("Tags added to matching scenarios where they did not exist already.")
