"""
main.py
* This file is auto-formated using BLACK
"""

from datetime import datetime
import data
import random
from typing import Optional, List, Dict, Union

StrInt = Union[str, int]


class Application:
    welcome_message: str = "Welcome to Python Institute's elementary arithmetic examination."
    helper_reminder: str = '-Type "help" to see available commands.\n'

    user_id: Optional[str] = None
    category: Optional[str] = None
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
            self.category = self.change_subject()
        # for multiple-test takers, category change is prompted
        else:
            while True:
                subject_change = input("Change category? [Y/N]")
                if subject_change.lower() == 'y' or subject_change.lower() == 'n':
                    break
            if subject_change == 'y':
                self.category = self.change_subject()

        # administers test questions until the end of the specific test length
        for i in range(self.test_length):
            self.current_question = self.generate_question(self.category)
            self.asked_questions.append(self.current_question)

            # ask the question
            self._ask_question()
            # checks and records answer
            self._check_answer()

        # provides feedback to the user and logs the results
        print(f"** You've answered {self.correct} of {self.correct + self.incorrect} questions correctly. **")
        self.save_file(self.user_id, self.category, str(self.correct) + "/" + str(self.correct + self.incorrect))

        # reset values
        self.correct = 0
        self.incorrect = 0

        # recursive call for additional tests
        while True:
            continue_input = input("Would you like to take another test? [Y/N]")
            if continue_input.lower() == 'y' or continue_input.lower() == 'n':
                if continue_input.lower() == 'y':
                    self.administer_test()
                    break
                else:
                    break

    def _check_answer(self):
        """
        checks the user answer

        :return: None
        """
        # TODO: remove use of str slicing and eval -- good for now, low priority, but too many ways this could go wrong
        correct_answer = eval(self.current_question[8:-3])
        if correct_answer == self.current_answer:
            self.correct += 1
            print('correct', end=" || ")
        else:
            self.incorrect += 1
            print(f'incorrect (the answer is {correct_answer})', end=" || ")
        print(f'{self.correct} correct : {self.incorrect} incorrect')

        return

    def _ask_question(self):
        """
        prompts the user with the question and recurses on invalid input

        :return: None
        """
        self.current_answer = input(self.current_question)
        if not self.current_answer.lstrip('-').isdigit():
            print("Please provide a valid answer.")
            return self._ask_question()
        else:
            self.current_answer = int(self.current_answer)

        return

    # generates pseudo-unique, randomized operands
    def generate_question(self, category: str, difficulty: str = "easy"):
        """
        generate a question to ask the user

        :param category str: the arithmetic category selected by the user
        :param difficulty str: the difficulty level; defaults to 'easy'
        :return str: string representation of question
        """
        while True:  # do-while in python
            if difficulty == "easy":
                if category != "/":
                    if category == "+" or category == "-":
                        lower_range = 0 + self.pi_factor
                        upper_range = 100 * self.pi_factor
                    elif category == "*":
                        lower_range = 0 + self.pi_factor
                        upper_range = 10 * self.pi_factor
                    else:
                        break

                    num1 = random.randint(lower_range, upper_range)
                    num2 = random.randint(lower_range, upper_range)

                elif category == "/":
                    lower_range = 3 * self.pi_factor
                    upper_range = 100 * self.pi_factor
                    nums = [random.randint(lower_range, upper_range), random.randint(lower_range, upper_range)]
                    # restricts answer to int and >2
                    while (max(nums) % min(nums) != 0) or (max(nums) / min(nums) < 3):
                        nums = [random.randint(lower_range, upper_range), random.randint(lower_range, upper_range)]
                    num1 = max(nums)
                    num2 = min(nums)

                else:
                    break

                # checks for pseudo-uniqueness
                question = f"What is {num1} {category} {num2}?  "
                if question not in self.asked_questions:
                    return question

    def change_subject(self):
        """
        requests user select the test category
        returns selected category
        accepts either words (eg "addition") or symbols (eg "+")

        :return str: subject to be examined selected by user
        """
        display_message = (
            'Please identify examination type:\n'
            '\t"addition"\t\tor\t"+"\n'
            '\t"subtraction"\t\tor\t"-"\n'
            '\t"multiplication"\tor\t"*"\n'
            '\t"division"\t\tor\t"/"\n'
        )

        while True:
            subject = input(display_message)
            if subject.lower() in self.valid_subjects.keys() or subject.lower() in self.valid_subjects.values():
                break
            print("Invalid entry.")

        # parse user input
        if len(subject) > 1:
            selection = subject
            subject = self.valid_subjects[selection]
        else:
            selection = [k for k, v in self.valid_subjects.items() if subject == v][0]

        print(f"{selection.capitalize()} has been selected.")
        return subject

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

    @staticmethod
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
