import sys
import utility

with open(sys.argv[1], "r") as input_file:
    input_data = input_file.readlines()

utility.parse_input(input_data)
print(utility.states)

for state in utility.states.values():
    print(state)
    print(state.avail_actions)

