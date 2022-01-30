"""
main.py
* This file is auto-formated using BLACK
"""

from datetime import datetime
import data
import random
from typing import Optional, List, Dict, Union, Callable
import operator
from dataclasses import dataclass


StrInt = Union[str, int]


@dataclass
class Question:
    num1: int
    num2: int
    question_type: str

    operator_mapping = {
        '+': {'callable': operator.add, 'opposite_callable': operator.sub},
        '-': {'callable': operator.sub, 'opposite_callable': operator.add},
        '/': {'callable': operator.truediv, 'opposite_callable': operator.mul},
        '*': {'callable': operator.mul, 'opposite_callable': operator.truediv},
    }

    @property
    def operator_callable(self):
        return self.operator_mapping[self.question_type]['callable']

    @property
    def operator_opposite_callable(self):
        return self.operator_mapping[self.question_type]['opposite_callable']

    @property
    def operands(self):
        if self.question_type in ['/', '-']:
            operand2, answer = max(self.num1, self.num2), min(self.num1, self.num2)
            operand1 = self.operator_opposite_callable(answer, operand2)
        elif self.question_type in ['*', '+']:
            operand1, operand2 = min(self.num1, self.num2), max(self.num1, self.num2)
            answer = self.operator_callable(operand1, operand2)
        else:
            raise ValueError(f'invalid question type: {self.question_type}')

        return {'operand1': operand1, 'operand2': operand2, 'answer': answer}

    @property
    def question_string(self):
        return f"What is {self.operands['operand1']} {self.question_type} {self.operands['operand2']}?  "

    def check_answer(self, attempt):
        return True if attempt == self.operands['answer'] else False


class Application:
    welcome_message: str = "Welcome to Python Institute's elementary arithmetic examination."
    helper_reminder: str = '-Type "help" to see available commands.\n'

    user_id: Optional[str] = None
    category: Optional[str] = None
    category_string: Optional[str] = None
    difficulty: str = "easy"
    current_question: Optional[str] = None
    current_answer: Optional[StrInt] = None
    correct: int = 0
    incorrect: int = 0
    test_length: int = 3
    test_time: int = 10
    asked_questions: List[str] = []
    pi_factor: int = 1

    valid_subjects: Dict[str, str] = {"addition": "+", "subtraction": "-", "multiplication": "*", "division": "/"}

    help_text: str = ''.join([each for each in data.commands_box])
    help_text: str = help_text + ''.join(data.command_list)

    def __int__(self):
        pass

    def run(self):
        """
        mainloop
        :return:  None
        """
        print(self.welcome_message)
        while True:
            user_input = input(self.helper_reminder)
            self.parse_user_input(user_input)

    def administer_test(self):
        """
        administer the test to the user
        :return: None
        """
        # begins test by requesting user id and category
        if self.user_id is None:
            self.user_id = input("Please identify yourself: ")

        if self.category is None:
            self.change_subject()

        self._ask_questions()

        continue_input = self._ask_continue()
        if continue_input:
            # recursive call for additional tests
            self.administer_test()

        self._reset_values()

        return

    def _reset_values(self):
        self.correct = 0
        self.incorrect = 0

        return

    def _ask_questions(self):
        # administers test questions until the end of the specific test length
        for i in range(self.test_length):
            self.current_question = self.generate_question()
            self.asked_questions.append(self.current_question.question_string)

            # ask the question
            self._ask_question()
            # checks and records answer
            self._check_answer()

        # provides feedback to the user and logs the results
        print(f"** You've answered {self.correct} of {self.correct + self.incorrect} questions correctly. **")
        self.save_file(self.user_id, self.category, str(self.correct) + "/" + str(self.correct + self.incorrect))

        return

    def _ask_question(self):
        """
        prompts the user with the question and recurses on invalid input

        :return: None
        """
        self.current_answer = input(self.current_question.question_string)
        if not self.current_answer.lstrip('-').isdigit():
            print("Please provide a valid answer.")
            return self._ask_question()
        else:
            self.current_answer = int(self.current_answer)

        return

    def _check_answer(self):
        """
        checks the user answer

        :return: None
        """
        if self.current_question.check_answer(self.current_answer):
            self.correct += 1
            print('correct', end=" || ")
        else:
            self.incorrect += 1
            print(f'incorrect (the answer is {self.current_question.operands["answer"]})', end=" || ")
        print(f'{self.correct} correct : {self.incorrect} incorrect')

        return

    def _ask_continue(self):
        continue_input = input(f"Would you like to take another {self.category_string.capitalize()} test? [Y/N]").lower()
        if continue_input not in ('y', 'n'):
            return self.ask_continue()
        return True if continue_input == 'y' else False

    @property
    def number_ranges(self):
        ranges = {
            "+": {"lower": 0 + self.pi_factor, "upper": 100 * self.pi_factor},
            "-": {"lower": 0 + self.pi_factor, "upper": 100 * self.pi_factor},
            "*": {"lower": 0 + self.pi_factor, "upper": 10 * self.pi_factor},
            "/": {"lower": 3 * self.pi_factor, "upper": 10 * self.pi_factor},
        }
        return ranges

    @property
    def lower_range(self):
        return self.number_ranges[self.category]['lower']

    @property
    def upper_range(self):
        return self.number_ranges[self.category]['upper']

    def generate_question(self):
        """
        generate a question to ask the user
        generates pseudo-unique, randomized operands

        :param category str: the arithmetic category selected by the user
        :param difficulty str: the difficulty level; defaults to 'easy'
        :return: None
        """
        num1 = random.randint(self.lower_range, self.upper_range)
        num2 = random.randint(self.lower_range, self.upper_range)
        question = Question(num1, num2, self.category)
        if question in self.asked_questions:
            self.generate_question()
        return question

    def change_subject(self):
        """
        requests user select the test category
        returns selected category
        accepts either words (eg "addition") or symbols (eg "+")

        :return str: subject to be examined selected by user
        """
        formatted_operator_options = '\n'.join([f'\t{k}\t\tor\t{v}' for k, v in self.valid_subjects.items()])
        display_message = f'Please identify examination type:\n {formatted_operator_options}\n'
        subject = input(display_message)
        if subject.lower() not in self.valid_subjects.keys() and subject.lower() not in self.valid_subjects.values():
            print("Invalid entry.")
            return self.change_subject()

        # parse user input
        if subject in self.valid_subjects.keys():
            self.category_string = subject
            self.category = self.valid_subjects[subject]
        elif subject in self.valid_subjects.values():
            self.category_string = [k for k, v in self.valid_subjects.items() if subject == v][0]
            self.category = subject
        else:
            raise ValueError(f'Invalid entry: {subject}')

        print(f"{self.category_string.capitalize()} has been selected.")
        return

    def parse_user_input(self, user_input: str):
        """
        parses the user input to the main menu

        * not supported in auto-py-to-exe D:

        :param user_input str: The user input into the main menu
        :return: None
        """
        match user_input.lower():
            case 'help':
                print(self.help_text)
            case 'start' | 'start test':
                self.administer_test()
            case 'stop' | 'stop test':
                print("Not Implemented.")
            case 'difficulty' | 'change difficulty':
                print("Not Implemented.")
            case 'length':
                self.set_test_length()
            case 'logs':
                self.display_logs()
            case 'exit':
                quit()
            case 'pi':
                self.pi_factor = random.randint(1000, 10000)
                print("The difficulty has been adjusted accordingly.")
            case _:
                print('That command is not recognized as a valid input.')

    def set_test_length(self):
        """
        updates the length of the test

        :return: None
        """
        while True:
            self.test_length = input("Enter desired test length: ")
            if self.test_length.isdigit():
                self.test_length = int(self.test_length)
                if self.test_length > 0:
                    print(f"Test length has been changed to {self.test_length} questions.")
                    break

    # TODO: do ROT something for encrypted
    def save_file(self, user: str, category: str, score: str):
        """
        saves the users scores

        :param user str: the user name
        :param category str: the subject of the exam
        :param score str: the user score
        :return: None
        """
        file_header = "Examination Logs\n"

        try:
            file = open('user_data_logs.txt', 'x')
            file.close()
        except FileExistsError:
            pass

        file = open('user_data_logs.txt', 'r')
        if file.readline() == file_header:
            file_header = ""
        file.close()
        file = open('user_data_logs.txt', 'a')

        file.write(file_header)
        subject_name = [k for k, v in self.valid_subjects.items() if v == category][0]

        file.write(
            "User ID: "
            + str(user).title()
            + "\t\t"
            + "Topic: "
            + str(subject_name).capitalize()
            + "\t\t"
            + "Score: "
            + str(score)
            + "\t\t"
            + "Timestamp: "
            + str(datetime.now())
            + '\n'
        )
        file.close()

    # fn vs method; static
    # logs are not specific to instance ? etc
    def display_logs(self):
        """
        displays exam history

        :return: None
        """
        try:
            file = open('user_data_logs.txt', 'r')
        except FileExistsError:
            print("No log file exists.")
            return

        test_scores = file.readlines()
        for each in test_scores:
            print(each, end="")
        file.close()


if __name__ == "__main__":
    Application().run()
