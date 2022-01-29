""" this comment exists to fix comments below """

""" ### help text commands ### """
command_list = [
    "- start: ............. begin an examination.\n",
    "- stop: .............. halt the examination.\n",

    "- difficulty: ........ change difficulty (easy).\n",
    "- length: ............ change # of questions (3).\n",
    "- logs: .............. display examination logs.\n",
    "- pi: ................ informs the proctor you hail\n",
    "                       from the Python Institute.\n",
    "- exit: .............. exit the program.",
]

""" ### creating the dynamic command box ### """
border_dic = {"bottom_left": '\u2514', "vertical": '\u2502', "top_left": '\u250C',
              "horizontal": '\u2500', "top_right": '\u2510', "bottom_right": '\u2518'}

# the "commands_box" scales to max "command_list" length
max_width = 0
for each in command_list:
    if len(each) > max_width:
        max_width = len(each)
max_width = max_width - (max_width % 2)  # make even
max_width = max(max_width, (len("commands") + 2))  # lower boundary of 10

top_mid = ''.join([border_dic["horizontal"] for i in range(max_width - 2)])
top_line = border_dic["top_left"] + top_mid + border_dic["top_right"]

middle_middle_range = int(max_width / 2 - len("commands") / 2)
filler = ''.join([" " for i in range(middle_middle_range - 1)])
middle_line = border_dic["vertical"] + filler + "commands" + filler + border_dic["vertical"]

bottom_mid = ''.join([border_dic["horizontal"] for i in range(max_width - 2)])
bottom_line = border_dic["bottom_left"] + bottom_mid + border_dic["bottom_right"]

commands_box = [top_line + '\n', middle_line + '\n', bottom_line + '\n']
