from Display import Display
import matplotlib.pyplot as plt
import math

# A class that generates a Mapping file given LIDARPoints and FlightPath data
class Mapping:

    test_mode = False
    transferred_points_list = []
    min_distance = 0.2
    min_deviation = 0.001
    min_line_deviation = 0.005

    def __init__(self, test_mode=False):
        print("Initiated Mapping, test mode = {}".format(test_mode))
        self.test_mode = test_mode
        ds = Display()
        ds.loadFiles()
        ds.convert_files()
        self.transferred_points_list = ds.transferred_points_list

    # check if two lines are on the same x/y axis
    def x_continuous_judgement(self, prev_x, prev_y, curr_x, curr_y):
        if abs(prev_x - curr_x) < self.min_distance and abs(prev_y - curr_y) < self.min_deviation:
            return True
        else:
            return False

    def y_continuous_judgement(self, prev_x, prev_y, curr_x, curr_y):
        if abs(prev_y - curr_y) < self.min_distance and abs(prev_x - curr_x) < self.min_deviation:
            return True
        else:
            return False

    # sort two lines based on their positions
    def x_sort_points(self, x1, y1, x2, y2):
        if x1 < x2:
            return ([(x1, y1), (x2, y2)])
        else:
            return ([(x2, y2), (x1, y1)])

    def y_sort_points(self, x1, y1, x2, y2):
        if y1 < y2:
            return ([(x1, y1), (x2, y2)])
        else:
            return ([(x2, y2), (x1, y1)])

    # update the start/end points of new merged lines
    def x_update_start(self, x1, y1, x2, y2):
        if x1 < x2:
            return (x1, y1)
        else:
            return (x2, y2)

    def y_update_start(self, x1, y1, x2, y2):
        if y1 < y2:
            return (x1, y1)
        else:
            return (x2, y2)

    def x_update_end(self, x1, y1, x2, y2):
        if x1 > x2:
            return (x1, y1)
        else:
            return (x2, y2)

    def y_update_end(self, x1, y1, x2, y2):
        if y1 > y2:
            return (x1, y1)
        else:
            return (x2, y2)

    # NOTE: x_lines: horizontal lines; y_lines: vertical lines
    x_lines = []
    y_lines = []
    scattered_list = []

    # try to find relation between new dots and existing lines/scattered dots
    def find_relation(self, x, y):
        # initialize
        if not self.x_lines and not self.y_lines and not self.scattered_list:
            self.scattered_list.append((x, y))
        # appending points process
        else:
            found_match = False
            # try to find relation with x_lines
            if self.x_lines:
                for i, [(start_x, start_y), (end_x, end_y)] in enumerate(self.x_lines):
                    if self.x_continuous_judgement(start_x, start_y, x, y):
                        self.x_lines[i] = [self.x_update_start(start_x, start_y, x, y), (end_x, end_y)]
                        found_match = True
                        break
                    elif self.x_continuous_judgement(end_x, end_y, x, y):
                        self.x_lines[i] = [(start_x, start_y), self.x_update_end(end_x, end_y, x, y)]
                        found_match = True
                        break

            # try to find relation with y_lines
            if self.y_lines:
                for i, [(start_x, start_y), (end_x, end_y)] in enumerate(self.y_lines):
                    if self.y_continuous_judgement(start_x, start_y, x, y):
                        self.y_lines[i] = [self.y_update_start(start_x, start_y, x, y), (end_x, end_y)]
                        found_match = True
                        break
                    elif self.y_continuous_judgement(end_x, end_y, x, y):
                        self.y_lines[i] = [(start_x, start_y), self.y_update_end(end_x, end_y, x, y)]
                        found_match = True
                        break

            # try to find relation with scattered dots
            if self.scattered_list:
                for i, (scattered_x, scattered_y) in enumerate(self.scattered_list):
                    if self.x_continuous_judgement(scattered_x, scattered_y, x, y):
                        self.x_lines.append(self.x_sort_points(scattered_x, scattered_y, x, y))
                        del self.scattered_list[i]
                        found_match = True
                        break
                    elif self.y_continuous_judgement(scattered_x, scattered_y, x, y):
                        self.y_lines.append(self.y_sort_points(scattered_x, scattered_y, x, y))
                        del self.scattered_list[i]
                        found_match = True
                        break

            # if no relation found, add to the scattered list
            if not found_match:
                self.scattered_list.append((x, y))

    # draw lines based on the scanned dots provided
    def draw_lines(self):
        for scan in self.transferred_points_list:
            for (x, y) in scan:
                self.find_relation(float(x), float(y))
        if self.test_mode:
            print(self.x_lines)
            print(self.y_lines)

    # check if two lines are overlapping; if yes then return the new line; return False otherwise
    def x_overlap(self, line1, line2):
        line1_x1 = float(line1[0][0])
        line1_y1 = float(line1[0][1])
        line1_x2 = float(line1[1][0])
        line1_y2 = float(line1[1][1])
        line2_x1 = float(line2[0][0])
        line2_y1 = float(line2[0][1])
        line2_x2 = float(line2[1][0])
        line2_y2 = float(line2[1][1])

        if line1_x1 > line2_x2 and line1_x2 > line2_x2:
            return False
        elif line2_x1 > line1_x2 and line2_x2 > line1_x2:
            return False
        elif abs(line1_y1 - line2_y2) > 0.005:
            return False
        else:
            y_mean = (line1_y1 + line1_y2 + line2_y1 + line2_y2) / 4
            return [(min(line1_x1, line2_x1), y_mean), (max(line1_x2, line2_x2), y_mean)]

    def y_overlap(self, line1, line2):
        line1_x1 = float(line1[0][0])
        line1_y1 = float(line1[0][1])
        line1_x2 = float(line1[1][0])
        line1_y2 = float(line1[1][1])
        line2_x1 = float(line2[0][0])
        line2_y1 = float(line2[0][1])
        line2_x2 = float(line2[1][0])
        line2_y2 = float(line2[1][1])

        if line1_y1 > line2_y2 and line1_y2 > line2_y2:
            return False
        elif line2_y1 > line1_y2 and line2_y2 > line1_y2:
            return False
        elif abs(line1_x1 - line2_x2) > self.min_line_deviation:
            return False
        else:
            x_mean = (line1_x1 + line1_x2 + line2_x1 + line2_x2) / 4
            return [(x_mean, min(line1_y1, line2_y1)), (x_mean, max(line1_y2, line2_y2))]

    # merge lines that are overlapping
    def x_merging(self, lines):
        for i, line1 in enumerate(lines):
            for j, line2 in enumerate(lines):
                if i != j:
                    if self.x_overlap(line1, line2):
                        return self.x_overlap(line1, line2), i, j
        return [], i, j

    def y_merging(self, lines):
        for i, line1 in enumerate(lines):
            for j, line2 in enumerate(lines):
                if i != j:
                    if self.y_overlap(line1, line2):
                        return self.y_overlap(line1, line2), i, j
        return [], i, j

    # a filter that dumps single dots
    def dot_filter(self):
        temp_list = []
        for line in self.x_lines:
            if float(line[0][0]) != float(line[1][0]) or float(line[0][1]) != float(line[1][1]):
                temp_list.append(line)
        self.x_lines = temp_list
        for line in self.y_lines:
            if float(line[0][0]) != float(line[1][0]) or float(line[0][1]) != float(line[1][1]):
                temp_list.append(line)
        self.y_lines = temp_list

    # algorithm that merges overlapped lines
    def grouping(self):
        while True:
            new_line, i, j = self.x_merging(self.x_lines)
            if not new_line:
                break
            del self.x_lines[j]
            del self.x_lines[i]
            self.x_lines.append(new_line)
        while True:
            new_line, i, j = self.y_merging(self.y_lines)
            if not new_line:
                break
            del self.y_lines[j]
            del self.y_lines[i]
            self.y_lines.append(new_line)

        self.dot_filter()

    # visualize the Mapping result
    def print_scans(self):

        plt.figure(0)
        axes = plt.gca()
        axes.set_xlim([0, 25])
        axes.set_ylim([0, 20])

        # plotting the points
        for [(x1, y1), (x2, y2)] in self.x_lines:
            plt.plot([x1,x2], [y1,y2])
        for [(x1, y1), (x2, y2)] in self.y_lines:
            plt.plot([x1,x2], [y1,y2])

        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('Mapping for the room')
        plt.show()

    # round up the centimeter floats to milimeter ints
    def round_up_milimeter(self, n1, n2, n3, n4):
        return int(n1 * 100), int(n2 * 100), int(n3 * 100), int(n4 * 100)

    # method that write the result to Mapping.csv
    def output_result(self):
        with open('Mapping.csv', 'w') as f:
            for line in self.x_lines:
                xs, xe, ys, ye = self.round_up_milimeter(line[0][0], line[0][1], line[1][0], line[1][1])
                f.write("xstart: {} ystart: {} xend: {} yend: {}\n".format(xs, xe, ys, ye))
            for line in self.y_lines:
                xs, xe, ys, ye = self.round_up_milimeter(line[0][0], line[0][1], line[1][0], line[1][1])
                f.write("xstart: {} ystart: {} xend: {} yend: {}\n".format(xs, xe, ys, ye))

