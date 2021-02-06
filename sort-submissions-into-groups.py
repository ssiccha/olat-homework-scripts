#!/usr/bin/env python3

import os, csv, sys, subprocess

from find_student import find_student

# The GROUPS_FILE must be a csv file with columns
# "Vorname", "Nachname", and "Gruppe"
GROUPS_FILE = './mfi-ags-homework/gruppenzuordnungen.csv'
TARGET_DIRECTORY = 'mfi-ags-homework'

if len(sys.argv) != 2:
    raise Exception('usage: sort-homework.py <sheet-number>')

sheet_nr = sys.argv[1]
sheet_dir = "./" + "blatt-" + str(sheet_nr) + '/'

def substitute_umlauts(s):
    s = s.replace('ö', 'oe')
    s = s.replace('ä', 'ae')
    s = s.replace('ü', 'ue')
    return s

with open(GROUPS_FILE, mode='r') as csvFile:
    table = list(csv.DictReader(csvFile))
    student_count = 0
    missing_student = False
    for submission in os.listdir(sheet_dir):
        if (submission.startswith('gruppe')
                or not os.path.isdir(sheet_dir + submission)):
            continue
        student = find_student(submission, table)
        if student != False:
            student_count += 1
            src = sheet_dir + submission
            print(src)
            gruppe = student["Gruppe"]
            dst = sheet_dir + 'gruppe-' + gruppe
            subprocess.check_call(['mkdir', '-p', dst])
            subprocess.check_call(['rsync', '-auq', src, dst])
            subprocess.check_call(['rm', '-r', src])
        else:
            missing_student = True

    subprocess.check_call(['rsync', '-auq', sheet_dir[:-1], TARGET_DIRECTORY])
    if not missing_student:
        subprocess.check_call(['rm', '-r', sheet_dir])
    print('Sorted submissions of {} students'.format(student_count))
