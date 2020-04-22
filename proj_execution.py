import sys
import utility
import model_based
import model_free

with open(sys.argv[1], "r") as input_file:
    input_data = input_file.readlines()

utility.parse_input(input_data)
model_based.model_based_rl()
model_free.model_free_rl()


