from Display import Display
import sys


# A String to Boolean method
def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Cannot covert '{}' to a bool. arg1 should only be either 'True' or 'False'".format(s))


# Check if all arguments are typed in and run the program
try:
    if sys.argv[1]:
        is_test_mode = str_to_bool(sys.argv[1])
    else:
        is_test_mode = False

    if sys.argv[2] == 'all':
        scan_ID = sys.argv[2]
    elif int(sys.argv[2]) in range(0, 33):
        scan_ID = sys.argv[2]
    else:
        raise ValueError("Please fill in the second argument with the correct scan ID or 'all' to display all scans")

    ds = Display(is_test_mode, scan_ID)
    ds.loadFiles()
    ds.convert_files()
    ds.print_scans()

except IndexError:
    print("Please fill in all the arguments to continue.")