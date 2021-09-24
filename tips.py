from random import randint


def get_tips():
    with open("tips.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        lines[10] = lines[10].replace(r'\n', '\n')  #make the "\n"s a str literal

        return lines[randint(0,20)]
