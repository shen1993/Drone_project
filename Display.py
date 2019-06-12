import matplotlib.pyplot as plt
import math
import sys

# A Program that displays drone routes and LIDAR scans
class Display:

    lidar_points_list = []
    drone_path_list = []
    test_mode = False

    def __init__(self, test_mode = False):
        print("Initiated, test mode = {}".format(test_mode))
        self.test_mode = test_mode

    def loadFiles(self):
        # load LIDARPoints
        with open('LIDARPoints.csv', 'r') as f:

            for line in f:
                self.lidar_points_list.append(line.strip('\n').split(','))
            if self.test_mode:
                print(self.lidar_points_list)

        # load FlightPath
        with open('FlightPath.csv', 'r') as f:
            for line in f:
                self.drone_path_list.append(line.strip('\n').split(','))
            self.drone_path_list = self.drone_path_list[1::2]
            if self.test_mode:
                print(self.drone_path_list)

    transferred_points_list = []

    # Convert LIDARPoints to X/Y axis representation format
    def convert_files(self):

        temp_list = []
        counter = 0
        # a = angle, r = radius
        for [a, r] in self.lidar_points_list:
            curr_a = float(a)
            curr_r = float(r)
            x = curr_r / 1000 * math.cos(math.radians(curr_a)) + \
                float(self.drone_path_list[counter][0])
            y = curr_r / 1000 * -math.sin(math.radians(curr_a)) + \
                float(self.drone_path_list[counter][1])

            # new scan mark
            if r == '533' or r == '534':
                # print(curr_a)
                if temp_list != []:
                    counter += 1
                    self.transferred_points_list.append(temp_list)
                    temp_list = []
            else:
                temp_list.append((x, y))

        # Adding the final scan that wasn't being added to the list yet
        if temp_list != []:
            self.transferred_points_list.append(temp_list)

        print("Total of scans: {}".format(len(self.transferred_points_list)))

    # Print the selected scan(s)
    def print_scans(self):

        plt.figure(0)
        axes = plt.gca()
        axes.set_xlim([0, 25])
        axes.set_ylim([0, 20])

        x_list = []
        y_list = []

        for i, s in enumerate(self.transferred_points_list):
            for (x, y) in s:
                x_list.append(x)
                y_list.append(y)

        x_path = []
        y_path = []

        for i, s in enumerate(self.drone_path_list):
            x_path.append(float(s[0]))
            y_path.append(float(s[1]))

        # plotting the points
        plt.scatter(x_list, y_list, s=2)
        plt.plot(x_path, y_path, 'r')

        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('Drone Route Display')
        plt.show()

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

    ds = Display(is_test_mode)
    ds.loadFiles()
    ds.convert_files()
    ds.print_scans()

except IndexError:
    print("Please fill in all the arguments to continue.")
