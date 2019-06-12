import matplotlib.pyplot as plt
import math

# A Program that displays drone routes and LIDAR scans
class Display:

    lidar_points_list = []
    drone_path_list = []
    test_mode = False
    scan_ID = 'all'

    def __init__(self, test_mode = False, scan_ID = 'all'):
        print("Initiated, test mode = {}".format(test_mode))
        self.test_mode = test_mode
        self.scan_ID = scan_ID

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

        x_curr_list = []
        y_curr_list = []

        x_path = []
        y_path = []

        if self.scan_ID != 'all':
            for (x, y) in self.transferred_points_list[int(self.scan_ID)]:
                x_curr_list.append(x)
                y_curr_list.append(y)

            x_path.append(float(self.drone_path_list[int(self.scan_ID)][0]))
            y_path.append(float(self.drone_path_list[int(self.scan_ID)][1]))

        else:
            for s in self.drone_path_list:
                x_path.append(float(s[0]))
                y_path.append(float(s[1]))

        for s in self.transferred_points_list:
            for (x, y) in s:
                x_list.append(x)
                y_list.append(y)

        # plotting the points
        plt.scatter(x_list, y_list, s=2, color = 'cornflowerblue')
        plt.scatter(x_curr_list, y_curr_list, s=2, color = 'b')
        plt.scatter(x_path, y_path, s=10, color = 'r')
        plt.plot(x_path, y_path, 'orangered')

        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('Drone Route Display')
        plt.show()

