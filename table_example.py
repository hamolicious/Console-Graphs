from console_widgets import Table, align_left, align_right, align_center
from random import randint, choice
from os import system ; clear = lambda : system('cls') ; clear()

def rand_string():
    alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    length = randint(5, 15)

    return ''.join(choice(alphabet) for _ in range(length))

def generate_data():
    """
    Data needs to be in this format:
    data = [
        ["Name", other values, other values, other values],
        ["Name", other values, other values, other values],
        ["Name", other values, other values, other values],
        ["Name", other values, other values, other values],
        ["Name", other values, other values, other values],
    ]
    to add a header, simply make the first entry a header
    data = [
        ["Name of collumn", "Name of collumn", "Name of collumn", "Name of collumn"],
        ["Name",             other values,      other values,      other values],
        ["Name",             other values,      other values,      other values],
        ["Name",             other values,      other values,      other values],
        ["Name",             other values,      other values,      other values],
    ]
    """

    data = []
    data.append(['Name', 'Value', 'Other Value', 'Cooler Value']) # add headers

    for _ in range(10): # add data
        d = []

        d.append(rand_string())

        for _ in range(len(data[0])-1):
            d.append(randint(0, 10000))

        data.append(d)

    return data

data = generate_data()
table = Table(
    data, # the data as a 2 dimensional array where each row contains the collumns for the table
    use_colour=True, # select if you want colour output
    padding=1, # amount of white space to add inbetween each data entry
    align_data=align_left, # how to align data, can choose from align_left, align_right, align_center
    align_header=align_center, # how to align the first entry in the table, can choose from align_left, align_right, align_center
    add_total_row=True, # choose if you want an extra row to be added that calculates a value for each collumn
    add_mean_row=True, # choose if you want an extra row to be added that calculates a value for each collumn
    add_mode_row=True # choose if you want an extra row to be added that calculates a value for each collumn
)

table.update() # update to calculate the extra rows and sizing for the rows, fill out data and add colour
table() # prints the table to the console or you can use table.display()

print('\nThis example shows you how to use the table class')








