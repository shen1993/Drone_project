from Display import Display
from Mapping import Mapping
import sys


# A String to Boolean method
def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Cannot covert '{}' to a bool. arg2 should only be either 'True' or 'False'".format(s))

# The Display method
def display():
    is_test_mode = str_to_bool(sys.argv[2])

    if sys.argv[3] == 'all':
        scan_ID = sys.argv[3]
    elif int(sys.argv[3]) in range(0, 33):
        scan_ID = sys.argv[3]
    else:
        raise ValueError(
            "Please fill in the third argument with the correct scan ID or 'all' to display all scans")

    ds = Display(is_test_mode, scan_ID)
    ds.loadFiles()
    ds.convert_files()
    ds.print_scans()

# the Mapping method
def mapping():
    is_test_mode = str_to_bool(sys.argv[2])

    map = Mapping(is_test_mode)
    map.draw_lines()
    map.grouping()
    map.output_result()
    map.print_scans()

# Check if all arguments are typed in and run the program
try:
    if sys.argv[1] == 'Display':
        display()
    elif sys.argv[1] == 'Mapping':
        mapping()
    else:
        raise ValueError("Please fill in the first argument with 'Display' or 'Mapping'")

except IndexError:
    print("Please fill in all the required arguments to continue.")