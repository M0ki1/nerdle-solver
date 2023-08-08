import re

# Pattern stored in a variable
pattern_to_search = "e"

# Input string
string_to_search = "This is an EXAMPLE string."

# Method 1: Concatenate the variable with the regex expression
if re.search(r'{}'.format(pattern_to_search), string_to_search):
    print("Found '{}' in the string.".format(pattern_to_search))
else:
    print("Did not find '{}' in the string.".format(pattern_to_search))

# Method 2: Use an f-string (Python 3.6+)
if re.search(fr'{pattern_to_search}', string_to_search):
    print(f"Found '{pattern_to_search}' in the string.")
else:
    print(f"Did not find '{pattern_to_search}' in the string.")
