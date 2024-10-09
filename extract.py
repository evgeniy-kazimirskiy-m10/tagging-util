import re

# Input and output file paths
input_file_path = './com.m10.tests.integration.RunCucumberTestInCI.txt'
output_file_path = './failed_tests.txt'

# Regex to extract test case names with failure markers
test_case_regex = r'-- Time elapsed: .+ <<< (FAILURE|ERROR)!'

# Initialize a list to store failed test names
failed_tests = []

# Open the input file and process each line
with open(input_file_path, 'r', encoding='utf-8') as file:
  for line in file:
    if re.search(test_case_regex, line):
      # Extract the test case name (prior to "-- Time elapsed")
      test_case_name = line.split('-- Time elapsed:')[0].strip()
      failed_tests.append(test_case_name)

# Write the failed test cases to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
  for test_case in failed_tests:
    output_file.write(f"{test_case}\n")

print(f"Failed test cases have been extracted and saved to {output_file_path}")
