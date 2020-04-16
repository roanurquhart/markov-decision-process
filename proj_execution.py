import sys
import utility
import model_based

with open(sys.argv[1], "r") as input_file:
    input_data = input_file.readlines()

utility.parse_input(input_data)
model_based.model_based_rl()

# for state in utility.states.values():
#     print(state)
#     print(state.avail_actions)

