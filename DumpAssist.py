# Author: Argentix
# Description: A tool originally for practicing CEH Dumps but ended up as a general questions dump tool.
# It works with any multiple answers questions dump (text) file that has a question title, followed by the question and ends with the correct answer.
#
# Usage Ex: Enter file name (dump file): 312-50v10V12.0.txt
#           Enter question delimiter: . - (Exam Topic
#
# Usage Ex: Enter file name (dump file): 312-50v10V.txt
#           Enter question delimiter: NEW QUESTION
#
# Usage Ex: Enter file name (dump file): 312-50v10V12.0.txt
#           Session file found. Please select an option: 1
#           Random or in order? 1
#           Answer: a
#           Answer: progress
#           Answer: exit

import random
def parseQuestions(filename, delimiter):
    questions = {}
    with open(filename, "r") as dumpfile:
        state = "nothing"
        question = ""
        answer = ""
        questionID = 0
        for line in dumpfile.readlines():
            if delimiter in line:
                state = "question"
                questionID += 1
            if "Answer: " in line:
                state = "answer"
            if state == "question":
                question += line
            if state == "answer":
                answer = line.split("Answer: ")[1].strip()
                questions.update({questionID:{question:answer}})
                state = "nothing"
                question = ""
                answer = ""
        #printQuestions(questions)
    return questions

def greetUser():
    banner = """
    Dump assist v1.0
    This script keeps track of correctly answered questions in a .session file for each dump file.
    It firsts parses questions and answers from a commonly formatted dump file.
    In case the file has not been parsed before you will have to supply the question delimeter (a substring thats included in every question first line).
    If your file is a pdf you will need to convert it to a text file to work with (copy paste or use online converter).
    Type "progress" or "exit" as your answer at any time to see progress or exit.
    """
    print(banner)
    filename = input("Enter file name (dump file): ")
    session_file = filename  + ".session"
    try:
        with open(session_file, "r") as f:
            delimiter = f.readline().strip()
            file_exists = True
    except IOError:
        file_exists = False

    if file_exists:
        conflict = """
Session file found. Please select an option:
1. Continue last session
2. Start a new session
3. Start a new session with a new delimiter
"""
        option = input(conflict)
        if option == "2":
            with open(session_file, "w") as f:
                f.write(delimiter)
        if option == "3":
            with open(session_file, "w") as f:
                delimiter = input("Enter question delimiter: ")
                f.write(delimiter)
    else:
        with open(session_file, "w") as f:
            delimiter = input("Enter question delimiter: ")
            f.write(delimiter)
    questions = parseQuestions(filename, delimiter)
    start(questions, session_file)

def start(questions, session_file):
    with open(session_file, 'r+') as save:
        save.readline()
        checked_questions = save.readline().split(",")
        total_questions_num = len(questions)
        for questionID in questions.copy():
            if str(questionID) in checked_questions:
                questions.pop(questionID)
        starting_progress = (total_questions_num - len(questions)) / total_questions_num * 100
        option = input("Random or in order?\n1. Random\n2. In order\n")
        if option == "1":
            randomize = True
        else:
            randomize = False
        questions_iter = iter(list(questions.keys()))
        while True:
            current_question = 0
            progress = (total_questions_num - len(questions)) / total_questions_num * 100
            if randomize:
                current_question = random.choice(list(questions.keys()))
            else:
                current_question = next(questions_iter)
            q, a = list(questions[current_question].items())[0]
            print(f"Current question: {current_question}\n{q}")
            current_answer = input("Answer: ")
            if current_answer.lower() == "exit":
                print(f"progress saved in file {session_file}")
                exit()
            elif current_answer.lower() == "progress":
                print(f"Overall Progress: {(total_questions_num - len(questions))} out of {total_questions_num} ({int(progress)}%)")
                print(f"Progress this session: {int(progress - starting_progress)}%")
                current_answer = input("Answer: ")
            if current_answer.lower() == a.lower():
                questions.pop(current_question)
                save.write("," + str(current_question))
                save.flush()
                print("Correct!\n\n")
            else:
                print(f"Wrong! Correct answer is {a}\n\n")
        #printQuestions(questions)


def printQuestions(questions):
    for quid, question in questions.items():
        for q, a in question.items():
            print(f"---Question: {quid}---\n{q}\n---Answer---\n{a}")


greetUser()
