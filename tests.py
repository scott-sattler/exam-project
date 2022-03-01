import builtins
import datetime
import logging
import sys
import unittest
from itertools import chain

import kwargs as kwargs
from functools import partial
from unittest.mock import patch, MagicMock, call

import data
import main
import tests

""""
6.005 (in java) Notes @
https://ocw.mit.edu/ans7870/6/6.005/s16/classes/03-testing/index.html#documenting_your_testing_strategy

Formal reasoning about a program, usually called verification. Verification constructs a formal proof that a program is correct.
Code review. Having somebody else carefully read your code, and reason informally about it...
Testing. Running the program on carefully selected inputs and checking the results.

Specification: The specification describes the input and output behavior of the function.
Why do bugs often happen at boundaries? One reason is that programmers often make off-by-one mistakes (like writing <= instead of < , or initializing a counter to 0 instead of 1).

Why Software Testing is Hard:
    Exhaustive raw_input is infeasible.
    Haphazard raw_input is less likely to find bugs...
    Random or statistical raw_input does not work well for software.

Choosing Test Cases by Partitioning:
    To do this, we divide the input space into subdomains, each consisting of a set of inputs.
    ...partitioning the inputs as follows: 
        eg text.length(): 0, 1, > 1

Statement Coverage: is every statement run by some test case?
Branch Coverage: for every if or while statement in the program, are both the true and the false direction taken by some test case?
Path Coverage: is every possible combination of branches — every path through the program — taken by some test case?

Whitebox/Glass Box Testing: Whitebox raw_input (also called glass box raw_input) means choosing test cases with knowledge of how the function is actually implemented.
Blackbox Testing: Blackbox raw_input means choosing test cases only from the specification, not the implementation of the function. 

Document the strategy at the top of the test class...
Document how each test case was chosen, including white box tests...

Unit Test: A test that tests an individual module, in isolation if possible.
Integration Test: The opposite of a unit test is an integration test, which tests a combination of modules, or even the entire program. 
Stub: Isolating a higher-level module like makeIndex() is possible if we write stub versions of the modules that it calls. For example, a stub for getWebPage() wouldn’t access the internet at all, but instead would return mock web page content no matter what URL was passed to it. A stub for a class is often called a mock object. Stubs are an important technique when building large systems, but we will generally not use them in 6.005. 
    mock object
Regression Testing: Running all your tests after every change is called regression raw_input.
Automated raw_input: Automated raw_input means running the tests and checking their results automatically. A test driver should not be an interactive program that prompts you for inputs and prints out results for you to manually check. Instead, a test driver should invoke the module itself on fixed test cases and automatically check that the results are correct. The result of the test driver should be either “all tests OK” or “these tests failed: …” 
Automated Regression Testing: So automated regression raw_input is a best-practice of modern software engineering. 

Test-First Debugging: When a bug arises, immediately write a test case for it that elicits it, and immediately add it to your test suite. Once you find and fix the bug, all your test cases will be passing, and you’ll be done with debugging and have a regression test for that bug. 

In this reading, we saw these ideas:
    Test-first programming. Write tests before you write code.
    Partitioning and boundaries for choosing test cases systematically.
    White box raw_input and statement coverage for filling out a test suite.
    Unit-raw_input each module, in isolation as much as possible.
    Automated regression raw_input to keep bugs from coming back.
"""

# manual_inspection = True
manual_inspection = False


def helper_log_entry_to_dict_list(log_str_list, tests_taken):
    # suboptimal

    foobar = [{j.split(': ')[0]: j.split(': ')[1] for j in i}
              for i in [z.split(', ') for z in [y for y in map(lambda x: x.rstrip("\n"), log_str_list[-tests_taken:])]]]

    relevant_log_entries = log_str_list[-tests_taken:]
    # sub_1_rle = map(lambda x: x.rstrip("\n"), relevant_log_entries)
    sub_1_rle = [x.rstrip("\n") for x in relevant_log_entries]
    sub_2_rle = [x.split(', ') for x in sub_1_rle]
    sub_3_rle = [{y.split(': ')[0]: y.split(': ')[1] for y in x} for x in sub_2_rle]

    if sub_3_rle == foobar:
        return sub_3_rle
    else:
        raise AssertionError


class ApplicationTests(unittest.TestCase):
    """
    this testing is a learning exercise and intends to demonstrate ability
    scope of testing therefore coverage is heavily restricted

    method format:  'test_' +
                    'optional information'
                    + '_method_name'

    for pseudo-comprehensive input coverage:
        test max len(input)
        ...

    """

    # If nothing was entered then input/raw_input returns empty string.
    # TODO: move/use
    invalid_inputs = ['', ' ', 'y', 'n', 'yes', 'no']

    tested_app = main.Application()

    def __int__(self):
        pass

    # The setUp() and tearDown() methods allow you to define instructions
    #   that will be executed before and after each test method.

    # TODO: specification on all tests
    """
    specification:  input output behavior of function

    strategy:   test expected behavior of user input.
                patch input(),
                call tested method,
                check input calls,
                check user_id.
    
    note:   id restriction tested
    
    coverage:   not comprehensive
    """
    def test_set_user_id(self):
        # set_subject() tests
        number_of_tests = 3
        test_case_1 = ['foo']
        test_case_2 = ['', 'ralph']
        test_case_3 = ['', ' ', 'bar']
        # add test here ... and update number_of_tests
        test_cases = []
        for i in range(1, number_of_tests + 1):
            test_cases.append(eval('test_case_' + str(i)))

        for test_case in test_cases:
            # If nothing was entered then input/raw_input returns empty string.
            with patch('builtins.input', side_effect=test_case) as patched_input:
                self.tested_app.set_user_id()
                assert patched_input.call_count == len(test_case)
                assert self.tested_app.user_id == test_case[-1]

        return None

    """
    specification:  input output behavior of function
    
    strategy:   patch out input() and print()
                input side_effects simulate sequence of user inputs
                check return/non-locals: that correct subject is selected
                check input() and print() for expected behavior    
        
    coverage:   not comprehensive (not covered, eg: max # of inputs; max input length)
    """
    def test_set_subject(self):
        # set_subject() tests
        # noinspection PyUnusedLocal
        number_of_tests = 4
        test_sequence_1 = ['foo', '', 'addition']
        test_sequence_2 = [' ', 'no', 'yes', 'subtraction']
        test_sequence_3 = ['', ' ', '/']
        test_sequence_4 = ['*']
        # add test here ... and update number_of_tests
        test_sequences = []
        for i in range(1, number_of_tests + 1):
            test_sequences.append(eval('test_sequence_' + str(i)))

        user_prompt = data.set_subject_user_prompt
        invalid_message = self.tested_app.invalid_notification
        selection_message_unfilled = self.tested_app.selection_message

        # dict to list
        val_sub = main.Application.valid_subjects
        valid_subjects_list = [list(val_sub.items())[y][x] for x in [0, 1] for y in range(len(val_sub))]

        for test_sequence in test_sequences:
            subject_word = test_sequence[-1]
            if subject_word in val_sub.values():  # get word if symbol tested
                subject_word = [k for k, v in val_sub.items() if subject_word == v][0]

            selection_message = selection_message_unfilled.format(subject_word).capitalize()

            with patch('builtins.input') as patched_input, patch('builtins.print') as patched_print:
                patched_input.side_effect = test_sequence
                self.tested_app.set_subject()

                # non-local/returns
                assert self.tested_app.subject_word == subject_word
                assert self.tested_app.subject_symbol == val_sub[subject_word]

                # print()
                # on invalid input: invalid_message; on valid input: selection_message
                assert patched_print.call_count == len(test_sequence)
                user_input_translated_to_print_call_string = \
                    [selection_message if x in valid_subjects_list else invalid_message for x in test_sequence]
                user_input_translated_to_print_call = [call(x) for x in user_input_translated_to_print_call_string]
                assert patched_print.mock_calls == user_input_translated_to_print_call

                # input()
                # for each input request: user_prompt
                assert patched_input.call_count == len(test_sequence)
                user_input_translated_to_input_call = [call(user_prompt) for x in test_sequence]
                assert patched_input.mock_calls == user_input_translated_to_input_call

        return None

    """
    specification:  input output behavior of function
    
    strategy:   patch input
                provide simulated test input
                check log
                
    coverage: limited
    
    note:   print is patched to suppress output
    """
    def test_administer_test(self):
        # example test
        admin_test_user_input = {'user_id': 'user_test',
                                 'subject_symbol': '+',
                                 'first_ans': '-1',
                                 'second_ans': '-1',
                                 'third_ans': '-1',
                                 'continue': 'y',

                                 'first_ans_2': '-1',
                                 'second_ans_2': '-1',
                                 'third_ans_2': '-1',
                                 'continue_2': 'n'}

        inp_len = len(admin_test_user_input)
        tests_taken = int((inp_len - 2) / 4)

        # WARNING: assumes symbol used for testing
        symbol = admin_test_user_input['subject_symbol']
        subject_name = [k for k, v in data.valid_subjects.items() if v == symbol][0]

        # copy file contents prior to modification
        with open('user_data_logs.txt', 'r') as file:
            unmodified_lines = file.readlines()

        # example log
        # Session ID: 1646019377
        # User ID: User_Test_2      .title
        # Subject: Addition         .capitalize
        # Score: 0/3
        # Timestamp: 2022-02-24 19:39:03.400166

        # testing...
        with patch('builtins.input') as patched_input, patch('builtins.print'):
            patched_input.side_effect = list(admin_test_user_input.values())
            self.tested_app.administer_test()

        with open('user_data_logs.txt', 'r') as file:
            lines = file.readlines()

        converted_log_entries = helper_log_entry_to_dict_list(lines, tests_taken)
        for each_test in converted_log_entries:

            assert admin_test_user_input['user_id'].title() == each_test['User ID']
            assert str(subject_name).capitalize() == each_test['Subject']
            assert '/' + str(self.tested_app.test_length) in each_test['Score']

            stamp_time = datetime.datetime.strptime(each_test['Timestamp'][0:-7], '%Y-%m-%d %H:%M:%S')
            assert datetime.datetime.now() - stamp_time < datetime.timedelta(minutes=1)

        # restore log to state prior to testing
        with open('user_data_logs.txt', 'w') as file:
            file.writelines(unmodified_lines)

        return None

    """
    specification:  input output behavior of function
    
    strategy:   test expected behavior of menu commands.
                patch out the function that should be called,
                test if patched function was called.
    
    note:   (?)all in app calls are made without arguments
    """
    def test_parse_user_input(self):
        # valid_user_inputs = self.tested_app.valid_subjects
        input_call_dict = {
            'help': None,
            'start': 'administer_test',
            'stop': None,
            'difficulty': None,
            'length': 'set_test_length',
            'logs': 'display_logs',
            'exit': None,
            'pi': None
        }  # missing | alts
        # pi factor different case (just check global no longer default), !also print().
        # pi factor can use the .call_args (below)

        sieved_input_call_dict = {k: v for k, v in input_call_dict.items() if v is not None}

        for each_command in sieved_input_call_dict:
            patch_string = 'main.Application.' + sieved_input_call_dict[each_command]
            with patch(patch_string) as patched_method:
                self.tested_app.parse_user_input(each_command)
                assert patched_method.called
                assert patched_method.call_args[0] == ()

        print('skipped methods:', [k for k, v in input_call_dict.items() if v is None],
              end='\n\n') if manual_inspection else None  # debug

        return None


if __name__ == "__main__":
    unittest.main()

# dir(tests.ApplicationTests)
methods_tested = [x for x in dir(tests.ApplicationTests) if x.startswith('test_')]
methods_to_test = [x for x in dir(main.Application) if not x.startswith('__') and callable(getattr(main.Application, x))]
print(f'tests remaining: {len(methods_to_test)}', methods_to_test, sep='\n')
