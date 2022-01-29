""" main.py """

from datetime import datetime
import data
import random


# when exactly use __int__ declarations and, uh, normal declarations under class
# methods vs functions, when and where
# fn vs method; static
# logs are not specific to instance ? etc

class Application:
    var = None
    welcome_message = "Welcome to Python Institute's elementary arithmetic examination."
    helper_reminder = '-Type "help" to see available commands.\n'

    user_id = None
    category = None
    difficulty = "easy"
    current_question = None
    correct = 0
    incorrect = 0
    test_length = 3
    test_time = 10
    time_remaining = test_time
    asked_questions = []
    pi_factor = 1

    valid_subjects = {"addition": "+", "subtraction": "-", "multiplication": "*", "division": "/"}

    help_text = ''.join([each for each in data.commands_box])
    help_text = help_text + ''.join(data.command_list)

    def __int__(self):
        # self.category = None
        # self.current_question = None
        # self.correct = 0
        # self.incorrect = 0
        pass

    # mainloop
    def run(self):
        print(self.welcome_message)
        while True:
            user_input = input(self.helper_reminder)
            self.parse_user_input(user_input)

    def administer_test(self):
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
        while True and (self.correct + self.incorrect) < int(self.test_length):
            self.current_question = self.generate_question(self.category)
            self.asked_questions.append(self.current_question)

            while True:
                user_answer = input(self.current_question)
                if user_answer.lstrip('-').isdigit():
                    break
                else:
                    print("Please provide a valid answer.", end="\n")

            # checks and records answer
            user_answer = int(user_answer)
            correct_answer = int(eval(self.current_question[8:-3]))
            if correct_answer == user_answer:
                self.correct += 1
                print('correct', end=" || ")
            else:
                self.incorrect += 1
                print(f'incorrect (the answer is {correct_answer})', end=" || ")
            print(f'{self.correct} correct : {self.incorrect} incorrect')

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

    # generates pseudo-unique, randomized operands
    def generate_question(self, category, difficulty="easy"):
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

    # requests user select the test category
    # returns selected category
    # accepts either words (eg "addition") or symbols (eg "+")
    def change_subject(self):
        display_message = ('Please identify examination type:\n'
                           '\t"addition"\t\tor\t"+"\n'
                           '\t"subtraction"\t\tor\t"-"\n'
                           '\t"multiplication"\tor\t"*"\n'
                           '\t"division"\t\tor\t"/"\n')

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

    def parse_user_input(self, user_input):
        # not supported in auto-py-to-exe D:
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
        while True:
            self.test_length = input("Enter desired test length: ")
            if self.test_length.isdigit():
                self.test_length = int(self.test_length)
                if self.test_length > 0:
                    print(f"Test length has been changed to {self.test_length} questions.")
                    break

    def save_file(self, user, category, score, encrypted=False):
        # do ROT something for encrypted

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

        file.write("User ID: " + str(user).title() + "\t\t" +
                   "Topic: " + str(subject_name).capitalize() + "\t\t" +
                   "Score: " + str(score) + "\t\t" +
                   "Timestamp: " + str(datetime.now()) + '\n')
        file.close()

    # fn vs method; static
    # logs are not specific to instance ? etc
    def display_logs(self):
        try:
            file = open('user_data_logs.txt', 'r')
        except FileExistsError:
            print("No log file exists.")
            return

        test_scores = file.readlines()
        for each in test_scores:
            print(each, end="")
        file.close()


Application().run()
