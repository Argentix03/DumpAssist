"""Author: Argentix
Description: A tool originally for practicing CEH Dumps 
but ended up as a general questions dump tool.

It works with any multiple answers questions dump (text) file 
that has a question title, 
followed by the question and ends with the correct answer.

Usage Ex: Enter file name (dump file): 312-50v10V12.0.txt
          Enter question delimiter: . - (Exam Topic

Usage Ex: Enter file name (dump file): 312-50v10V.txt
          Enter question delimiter: NEW QUESTION

Usage Ex: Enter file name (dump file): 312-50v10V12.0.txt
          Session file found. Please select an option: 1
          Random or in order? 1
          Answer: a
          Answer: progress
          Answer: exit
"""
import random
import time


BANNER = """Dump assist v1.0
         This script keeps track of correctly answered questions in a .session file
         for each dump file.
         It first parses questions and answers from a commonly formatted dump file.
         In case the file has not been parsed before, 
         you will have to supply the question delimeter (a substring thats included
         in every question first line).
         If your file is a pdf you will first need to convert it into a text file
         to work with (copy paste or use online converter).
         Type "progress" or "exit" as your answer at any time to see progress or exit.
         """


SESSION_SELECTION = """Session file found. Please select an option:
    1. Continue last session
    2. Start a new session
    3. Start a new session with a new delimiter
    """


def parse_questions(filename, delimiter):
    """Return a dictionary of questions, answers and question IDs."""
    questions = {}
    with open(filename, "r") as dumpfile:
        state = "nothing"
        question, answer = "", ""
        question_id = 0
        for line in dumpfile.readlines():
            if delimiter in line:
                state = "question"
                question_id += 1
            if "Answer: " in line:
                state = "answer"
            if state == "question":
                question += line
            if state == "answer":
                answer = line.split("Answer: ")[1].strip()
                questions.update({question_id: {question: answer}})
                state = "nothing"
                question, answer = "", ""
        # print_questions(questions)
    return questions


def get_delimiter(session_file):
    """Extract the delimiter from the session file and return it.
    
    If the session file doesn't exist, return False.
    """
    try:
        with open(session_file, "r") as f:
            delimiter = f.readline().strip()
            return delimiter
    except IOError:
        return False


def write_to_session_file(session_file, delimiter):
    """Write the delimiter to the session file."""
    with open(session_file, "w") as f:
        f.write(delimiter + '\n')


def greet_user():
    """Search the session file, ask the user for instructions and start quiz.
    
    If the session file is found, the user can choose to continue his/her
    last session or to start a new one.
    If it's not found, a new one is made.
    After the configuration, the questions are extracted and the quiz begins.
    """
    print(BANNER)
    filename = input("Enter file name (dump file): ")
    session_file = filename + ".session"
    delimiter = get_delimiter(session_file)

    if delimiter:
        user_selection = input(SESSION_SELECTION)
        if user_selection == "2":
            write_to_session_file(session_file, delimiter)
        if user_selection == "3":
            new_delimiter = input("Enter question delimiter: ")
            write_to_session_file(session_file, new_delimiter)
    else:
        new_delimiter = input("Enter question delimiter: ")
        write_to_session_file(session_file, new_delimiter)

    questions = parse_questions(filename, delimiter)
    start_quiz(questions, session_file)


def remove_done_questions(questions, session_file):
    """Return the unsolved questions of the current session."""
    with open(session_file, 'r+') as session:
        session.readline()
        done_questions = session.readline().split(",")
        all_questions = questions.copy()
        for question_id in all_questions:
            if str(question_id) in done_questions:
                questions.pop(question_id)
    return questions


def is_random():
    """Returns True if the user wants the questions to be in a random order""" 
    questions_order = input(
                    "Random or in order?\n1. Random\n2. In order\n")
    if questions_order == "1":
        return True
    return False


def next_question(questions, questions_iter, randomize):
    """Return the next question from the questions iterator."""
    next_question = 0
    if randomize:
        next_question = random.choice(list(questions.keys()))
    else:
        next_question = next(questions_iter)
    return next_question


def print_progress(questions_sum, questions_left, starting_progress, progress):
    """Print the user's overall progress and this session's progress."""
    print(f"Overall Progress: "
          + f"{(questions_sum - len(questions_left))} "
          + f"out of {questions_sum} ({int(progress)}%)")
    print(f"Progress this session: "
          + f"{int(progress - starting_progress)}%")


def correct_answer(session_file, questions_left, question_index):
    """Add question number to session file and print a "Correct!" message."""
    questions_left.pop(question_index)
    with open(session_file, 'r+') as session:
        session.readline()
        session.write(str(question_index) + ',')
        session.flush()
    print("Correct!\n\n")


def ask_a_question(session_file, questions_sum, questions_left, question_index, starting_progress, progress):
    """Ask the user a question.
    
    If the user gets the right answer, 
    the question will be removed (moved to the session file).
    If the user gets it wrong, the correct answer will be printed.

    Other options: 
    "exit" - Quit the program
    "progress" - Print the user's progress.
    """
    question, answer = tuple(*questions_left[question_index].items())
    print(f"Current question: {question_index}\n{question}")
    users_answer = input("Answer: ")
    if users_answer.lower() == "progress":
        print_progress(questions_sum, questions_left, starting_progress, progress)
        users_answer = input("Answer: ")
    if users_answer.lower() == "exit":
        print(f"progress saved in file {session_file}")
        time.sleep(1)
        exit()
    if users_answer.lower() == answer.lower():
        correct_answer(session_file, questions_left, question_index)
    else:
        print(f"Wrong! Correct answer is {answer}\n\n")


def start_quiz(all_questions, session_file):
    """"""
    questions_sum = len(all_questions)
    questions_left = remove_done_questions(all_questions, session_file)
    starting_progress = (questions_sum
                            - len(questions_left)) / questions_sum * 100
    questions_iter = iter(list(questions_left.keys()))
    randomize = is_random()
    while True:
        progress = (questions_sum - len(questions_left)) / questions_sum * 100
        question_index = next_question(questions_left, 
                                         questions_iter, randomize)
        ask_a_question(session_file, questions_sum, questions_left,
                            question_index, starting_progress, progress)
    # print_questions(all_questions)


def print_questions(questions):
    """Print all the questionsand answers."""
    for quid, question in questions.items():
        for question, answer in question.items():
            print(f"---Question: {quid}---\n{question}\n---Answer---\n{answer}")


greet_user()
