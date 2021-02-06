#!/usr/bin/env -S python3 -B
# -S: env accepts two arguments, -B: python does not compile

import os, sys, csv, shutil, subprocess

from find_student import find_student

if len(sys.argv) != 2:
    raise Exception('usage : prepare-bulk-assessment.py' \
                    + '<corrections-folder>')

# The GROUPS_FILE must be a csv file with columns
# "Vorname", "Nachname", and "Benutzername"
GROUPS_FILE = '/home/sergio/Seafile/eda/eda-homework/students.csv'

# The corrections are taken from <corrections-folder> and distributed into
# a zip-file. That zip-file can then uploaded to Olat via "bulk assessment /
# Massenbewertung".
# <corrections-folder> has to be the folder downloaded from Olat, but
# containing the corrections instead of the submissions.
CORRECTIONS_DIR = sys.argv[1] + '/'
UPLOAD_DIR = '__upload-to-olat/'

def students_with(table, column, value):
    result = []
    for student in table:
        if (student[column] == value):
            result.append(student)
    return result

def student_with_username(table, value):
    students = students_with(table, 'Benutzername', value)
    if (len(students) == 0):
        raise Exception('No student found with username ' + value)
    return students[0]

def students_with_submission_group(table, value):
    return students_with(table, 'Abgabegruppe', value)

def copy_corrections(submission, group):
    for student in group:
        dst = UPLOAD_DIR + student['Benutzername']
        if not (os.path.isdir(dst)):
            os.mkdir(dst)
        src_files = os.listdir(CORRECTIONS_DIR + submission)
        src_files = [CORRECTIONS_DIR + submission + '/' + src for src in src_files]
        for src in src_files:
            shutil.copy(src, dst)

def main():
    with open(GROUPS_FILE, mode='r') as csvFile:
        table = list(csv.DictReader(csvFile))
        if (not os.path.isdir(UPLOAD_DIR)):
            os.mkdir(UPLOAD_DIR)
        nr_groups_handled = 0
        for submission in os.listdir(CORRECTIONS_DIR):
            # username = find_username(submission, table)
            # student = student_with_username(table, username)
            student = find_student(submission, table)
            group_nr = student['Abgabegruppe']
            group = students_with_submission_group(table, group_nr)
            copy_corrections(submission, group)
            nr_groups_handled += 1
    print('Distributed {} corrections'.format(nr_groups_handled))
    print('Zipping corrections.')
    # We have to first cd into the UPLOAD_DIR because in older Olat versions
    # there is a bug which leads to Olat otherwise not recognizing the contents
    # of the zip file correctly.
    subprocess.run('cd ' + UPLOAD_DIR + '; zip -r ../upload-to-olat.zip *',
                   shell = True)
    subprocess.run('rm -r ' + UPLOAD_DIR, shell = True)

main()
