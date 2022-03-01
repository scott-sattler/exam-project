from typing import Dict

"""
Contents:
1. 'help' text and command box construction
2. set_subject prompt construction and formatting
3. write file contents and formatting

"""

"""
1 ##########################################################
"""
""" ### help text commands ### """
# noinspection INSPECTION_NAME
command_list_description = [
    "- help: .............. list available commands.\n",
    "- start: ............. begin an examination.\n",
    "- stop: .............. halt the examination.\n",

    "- difficulty: ........ change difficulty (easy).\n",
    "- length: ............ change # of questions (3).\n",
    "- logs: .............. display examination logs.\n",
    "- pi: ................ informs the proctor you hail " +
                            "from the Python Institute.\n",
    "- exit: .............. exit the program.",
]

help_command_list = [each.rsplit(':')[0].lstrip('- ') for each in command_list_description]
# help_command_list = ['help',
#                      'start',
#                      'stop',
#                      'difficulty',
#                      'length',
#                      'logs',
#                      'pi',
#                      'exit']

""" ### creating the dynamic command box ### """
border_dic = {"bottom_left": '\u2514', "vertical": '\u2502', "top_left": '\u250C',
              "horizontal": '\u2500', "top_right": '\u2510', "bottom_right": '\u2518'}

# the "commands_box" scales to max "command_list_description" length
max_width = 0
for each in command_list_description:
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

""" ### creating the help_text ### """
help_text: str = ''.join([each for each in commands_box])
help_text: str = help_text + ''.join(command_list_description)

""" 
2 ##########################################################
"""
valid_subjects: Dict[str, str] = {"addition": "+", "subtraction": "-", "multiplication": "*", "division": "/"}

""" ### creating and formatting user_prompt in set_subject ### """
# formatting user_prompt alignment
# column size = max word length; aligned right, center, left
min_width = max([len(x) for x in valid_subjects.keys()])
formatted_operator_options = \
    '\n'.join([f'{k:>{min_width}}{"or":^{min_width}}{v:<{min_width}}' for k, v in valid_subjects.items()])

set_subject_user_prompt = f'Please identify examination type:\n{formatted_operator_options}\n'

""" 
3 ##########################################################
"""

log_contents = {'Session ID': '',
                'User ID': '',
                'Subject': '',
                'Score': '',
                'Timestamp': ''}


