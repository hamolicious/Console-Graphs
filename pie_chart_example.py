from console_widgets import Pie_Chart, Colours, reset
from random import randint, choice
from os import system ; clear = lambda : system('cls') ; clear()

def generate_data():
    data = []

    ratios = [randint(1, 10) for _ in range(4)]
    total_per_unit = sum(ratios) / len(ratios)

    colour = 1
    for ratio in ratios:
        data.append([ratio * total_per_unit, colour])
        colour += 1

    return data

data = generate_data()
pie_chart = Pie_Chart(
    data,
    radius=15,
    use_colour=True
)

pie_chart.update()
pie_chart.display()

print('\nThis example shows you how to use the pie chart class')
print(Colours.error + 'Unfortunately I am still trying to debug this class, it will work maybe 15% of the time' + reset())







