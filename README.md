# DumpAssist
A tool originally for practicing CEH Dumps but ended up as a general questions dump tool.
It works with any multiple answers questions dump (text) files that has a question title, followed by the question and ends with the correct answer.

This script keeps track of correctly answered questions in a .session file for each dump file.
It firsts parses questions and answers from a commonly formatted dump file.
In case the file has not been parsed before you will have to supply the question delimeter (a substring thats included in every question first line).
If your file is a pdf you will need to convert it to a text file to work with (copy paste or use online converter).
Type "progress" or "exit" as your answer at any time to see progress or exit.

### Usage Example:
Enter file name (dump file): 312-50v10V12.0.txt
Enter question delimiter: . - (Exam Topic

### Usage Example:
Enter file name (dump file): 312-50v10V.txt
Enter question delimiter: NEW QUESTION

### Usage Example:
Enter file name (dump file): 312-50v10V12.0.txt
Session file found. Please select an option: 1
Random or in order? 1
Answer: a
Answer: progress
Answer: exit

### Demo:
![example image](https://github.com/Argentix03/DumpAssist/raw/main/usage-example.png?raw=true)
