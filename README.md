# exam-project

Interview prompt at local company:
>Create a command line interface (CLI) in Python which proctors a math (arithmetic) test.
>
>It should ask the user if they want to addition, subtraction, multiplication, or division.
>
>It asks ten questions of the category chosen.
>
>It provides the score that the user received.
>
>It then asks the user if they want to take another one.

The default test length in my implementation is 3 questions. This can be changed prior to starting the test (see the 'help' command).

Gage made multiple improvements to my initial code, then suggested I develop unit tests for the project. I had not covered testing to any significant depth prior to writing the first implementation, and quickly realized that, while my implementation seemed easy enough to follow and was quick to write, testing would be needlessly difficult. Another large refactor was done to dramatically simplify testing.

Written in PyCharm 2021.3.1.
