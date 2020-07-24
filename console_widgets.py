from os import system
from math import sin, cos, radians, sqrt

# region colours
def fg(color):
    return '\033[38;5;%dm' % color


def bg(color):
    return '\033[48;5;%dm' % color


def reset():
    return '\033[0m'


class Colours():
    error = fg(9)

    highlight_1 = bg(232)
    highlight_2 = bg(234)

    header = bg(23)
# endregion

def map_to_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def generate_table_cap(mode, width):
    if mode == 'top':
        char = '_'
    if mode == 'bottom':
        char = '‾'
    if mode == 'middle':
        cap = '-' * int(width)
        return '+' + cap[1 : width-1] + '+'

    return char * int(width)

def align_left(data, space, padding):
    dl = abs(len(str(data)) - space)
    return (' ' * padding) + str(data) + (' ' * dl) + (' ' * padding) + '|'

def align_right(data, space, padding):
    dl = abs(len(str(data)) - space)
    return (' ' * padding) + (' ' * dl) + str(data) + (' ' * padding) + '|'

def align_center(data, space, padding):
    dl = abs(len(str(data)) - space)

    if dl % 2 == 0 : add_one = False
    else           : add_one = True

    return (' ' * padding) + (' ' * (int(dl / 2) + add_one)) + str(data) + (' ' * int(dl / 2)) + (' ' * padding) + '|'

class Table():
    def __init__(self, data, use_colour=True, padding=1, align_data=align_left, align_header=align_center, add_total_row=False, add_mean_row=False, add_mode_row=False):
        """Creates a table inside the console.

        Parameters:
        data (list): the data as a 2 dimensional array where each row contains the collumns for the table
        use_colour (bool): select if you want colour output
        padding (int): amount of white space to add inbetween each data entry
        align_data: how to align data, can choose from align_left, align_right, align_center
        align_header: how to align the first entry in the table, can choose from align_left, align_right, align_center
        add_*_rows (bool): choose if you want an extra row to be added that calculates a value for each collumn
        """

        self.data = data

        self.output = Colours.error + 'Please update the table' + reset()
        self.use_colour = use_colour
        if use_colour : system('color')

        self.add_total_row = add_total_row
        self.add_mean_row = add_mean_row
        self.add_mode_row = add_mode_row

        self.align_data = align_data
        self.align_header = align_header

        self.padding = padding

    def add_data(self, data):
        """
        Adds a row of data to the table
        """
        self.data.append(data)

    def update(self):
        rows = len(self.data)
        columns = len(self.data[0])

        totals = [0 for _ in range(columns)]
        totals[0] = 'Total'

        means = [0 for _ in range(columns)]
        means[0] = 'Mean'

        modes = [[0] for _ in range(columns)]
        modes[0] = 'Mode'

        # calculate extra lines
        for i in range(rows):
            data_row = self.data[i]
            for j in range(columns):
                if type(totals[j]) is not str and type(data_row[j]) is not str:
                    totals[j] += data_row[j]
                if type(means[j]) is not str and type(data_row[j]) is not str:
                    means[j] += data_row[j]
                if type(modes[j]) is not str and type(data_row[j]) is not str:
                    modes[j].append(data_row[j])

        for i in range(len(means)):
            if type(means[i]) is not str:
                means[i] = round(means[i] / rows, 3)

        for i in range(len(modes)):
            if type(modes[i]) is not str:
                length = len(modes[i])
                modes[i] = sorted(modes[i])[int(length/2)]

        if self.add_total_row:
            self.data.append(totals)
        if self.add_mean_row:
            self.data.append(means)
        if self.add_mode_row:
            self.data.append(modes)

        rows = len(self.data)
        columns = len(self.data[0])

        # calculate lengths
        data_lengths = [0 for _ in range(columns)]
        for i in range(rows):
            data_row = self.data[i]

            for j in range(columns):
                current_len = len(str(data_row[j]))
                previous_len = data_lengths[j]

                data_lengths[j] = max(current_len, previous_len)

        # generate table
        colour_flip_flop = True
        self.output = ''
        for i in range(rows):
            data_row = self.data[i]
            stringed_row = '|'

            if   self.use_colour and i == 0               : colour = Colours.header
            elif self.use_colour and colour_flip_flop     : colour = Colours.highlight_1 ; colour_flip_flop = not colour_flip_flop
            elif self.use_colour and not colour_flip_flop : colour = Colours.highlight_2 ; colour_flip_flop = not colour_flip_flop
            else                                          : colour = ''

            table_width = 0
            for j in range(columns):
                data = data_row[j]

                if i == 0:
                    stringed_row += self.align_header(data, data_lengths[j], self.padding)
                else:
                    stringed_row += self.align_data(data, data_lengths[j], self.padding)

                table_width = len(stringed_row)

            self.output += colour + stringed_row + '\n'

        self.output = generate_table_cap('top', table_width) + '\n' + self.output + generate_table_cap('bottom', table_width) + reset()

        if self.add_total_row or self.add_mean_row or self.add_mode_row:
            indexs = []
            for i in ['Total', 'Mean', 'Mode']:
                index = self.output.find(i)
                if index == -1:
                    indexs.append(10000)
                else:
                    indexs.append(index)
            index = min(indexs)-self.padding-1

            self.output = self.output[0 : index] + generate_table_cap('middle', table_width) + '\n' + self.output[index : len(self.output)] + reset()

    def display(self):
        """
        Prints the table
        """
        print(self.output)

class Pie_Chart():
    def __init__(self, data, radius, use_colour=True):
        self.data = data
        self.radius = radius
        self.canvas_size = (radius*2) + 5

        if use_colour : system('color')

        self.output = Colours.error + 'Please update the chart' + reset()

        self.temp = True

    def create_canvas(self):
        self.output = []

        for _ in range(self.canvas_size):
            row = []
            for _ in range(self.canvas_size):
                row.append('  ' + reset())
            self.output.append(row)

    def add_sector(self, angle_min, angle_max, colour):
        for angle in range(int(angle_min), int(angle_max)):
            for rad in range(self.radius, 0, -1):
                x = int((rad * cos(radians(angle))) + self.canvas_size/2)
                y = int((rad * sin(radians(angle))) + self.canvas_size/2)

                self.output[y][x] = bg(colour) + '  '

    def update(self):
        self.create_canvas()

        deg_start = 0
        save = 0
        for data in self.data:
            val, colour = data

            deg_end = map_to_range(val, 0, 100, 0, 360)
            deg_end += save

            self.add_sector(deg_start, deg_end, colour)

            save = deg_end
            deg_start = deg_end

    def display(self):
        temp = ''
        for i in range(self.canvas_size):
            for j in range(self.canvas_size):
                temp += self.output[i][j]
            temp += '\n' + reset()

        print(temp)

        for data in self.data:
            val, colour = data

            print((' ' * int(self.canvas_size)) + bg(colour) + '  ' + reset() + f'  Object: {val}%')







