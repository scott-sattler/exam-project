"""
main.py
* This file is auto-formated using BLACK
"""
import data
from datetime import datetime
import time
import random
from typing import Optional, List, Dict, Union, Callable
import operator
from dataclasses import dataclass
import re


# StrInt = Union[str, int]


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
    # TODO(?): string data case consistency
    welcome_message: str = "Welcome to Python Institute's elementary arithmetic examination."
    helper_reminder: str = '-Type "help" to see available commands.\n'
    help_text = data.help_text
    valid_subjects = data.valid_subjects
    invalid_notification = "Invalid entry."
    selection_message = "{} has been selected."

    difficulty: str = "easy"
    user_id: Optional[str | None] = None
    session_id: Optional[int | None] = None
    subject_word: Optional[str | None] = None
    subject_symbol: Optional[str | None] = None
    current_question: Optional[str | None] = None
    current_answer: Optional[str | int | None] = None  # TODO: allow int data type?
    asked_questions: List[str] = []  # TODO: or none?
    correct: int = 0
    incorrect: int = 0
    test_length: int = 3
    test_time: int = 10
    pi_factor: int = 1

    def __int__(self):
        # TODO: allow passing arguments at command line? eg user_id
        pass

    def run(self):
        """
        mainloop
        :return:  None
        """
        user_prompt = self.helper_reminder

        print(self.welcome_message)
        while True:
            user_input = input(user_prompt)
            self.parse_user_input(user_input)

    def set_user_id(self):
        user_prompt = "Please identify yourself: "

        invalid_input = True
        while invalid_input:
            user_id = input(user_prompt)
            invalid_input = not bool(re.match(r'\w+', user_id))

        # noinspection PyUnboundLocalVariable
        self.user_id = user_id

    def set_subject(self):
        """
        # TODO: rewrite this
        requests user select the test subject
        returns selected subject
        accepts either words (eg "addition") or symbols (eg "+")

        :return str: examination subject the user selected
        """
        valid_subjects = self.valid_subjects
        user_prompt = data.set_subject_user_prompt
        invalid_notification = self.invalid_notification
        selection_message = self.selection_message

        user_input = input(user_prompt)
        if user_input.lower() not in valid_subjects.keys() and user_input.lower() not in valid_subjects.values():
            print(invalid_notification)
            return self.set_subject()

        # parse user input of either word or symbol
        if user_input in valid_subjects.keys():  # parse word
            self.subject_word = user_input
            self.subject_symbol = valid_subjects[user_input]
        elif user_input in valid_subjects.values():  # parse symbol
            self.subject_word = [k for k, v in valid_subjects.items() if user_input == v][0]
            self.subject_symbol = user_input

        print(selection_message.format(self.subject_word.capitalize()))

    def administer_test(self):
        """
        administer the test to the user
        :return: None
        """
        if self.session_id is None:
            epoch_time = int(time.time())  # GH
            self.session_id = epoch_time

        # begins test by requesting user id and subject_symbol
        if self.user_id is None:
            self.set_user_id()

        if self.subject_symbol is None:
            self.set_subject()

        self._ask_questions()

        # save results and reset values
        score = str(self.correct) + "/" + str(self.correct + self.incorrect)
        self.save_file(self.session_id,
                       self.user_id,
                       self.subject_symbol,
                       score)
        self._reset_values()

        continue_input = self._ask_continue()
        if continue_input:
            # recursive call for additional tests
            self.administer_test()

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

        # provides feedback to the user
        print(f"** You've answered {self.correct} of {self.correct + self.incorrect} questions correctly. **")

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
        continue_input = input(f"Would you like to take another {self.subject_word.capitalize()} test? [Y/N]").lower()
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
        return self.number_ranges[self.subject_symbol]['lower']

    @property
    def upper_range(self):
        return self.number_ranges[self.subject_symbol]['upper']

    def generate_question(self):
        """
        generate a question to ask the user
        generates pseudo-unique, randomized operands

        :param subject_symbol str: the arithmetic subject_symbol selected by the user
        :param difficulty str: the difficulty level; defaults to 'easy'
        :return: None
        """
        num1 = random.randint(self.lower_range, self.upper_range)
        num2 = random.randint(self.lower_range, self.upper_range)
        question = Question(num1, num2, self.subject_symbol)
        if question in self.asked_questions:
            self.generate_question()
        return question

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
    def save_file(self, session: int, user: str, category: str, score: str):
        """
        saves the users scores

        :param user str: the user name
        :param subject_symbol str: the subject of the exam
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
        subject_name = [k for k, v in data.valid_subjects.items() if v == category][0]

        write_contents = data.log_contents.copy()
        write_contents['Session ID'] = str(session)
        write_contents['User ID'] = str(user).title()
        write_contents['Subject'] = str(subject_name).capitalize()
        write_contents['Score'] = str(score)
        write_contents['Timestamp'] = str(datetime.now())

        write_string = ', '.join([f'{k}{": "}{v}' for k, v in write_contents.items()])

        file.write(write_string + '\n')
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
