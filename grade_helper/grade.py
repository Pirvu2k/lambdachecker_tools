#!/usr/bin/python3.8
import argparse
import requests
import csv
import os
import sys

# include lambdachecker utils
sys.path.append('../utils')  
from utils import login, endpoints, get_problem_info, BearerAuth

def parse_args():
    parser = argparse.ArgumentParser(description='Helper CLI tool for easier grading of lambdachecker students.')
    parser.add_argument('student', type=str, help='id of student on lambdachecker or path to .csv file containing students')
    parser.add_argument('--problem-prefix', type=str, help='will show problems only if they have this prefix')
    parser.add_argument('--problems', nargs='*', help='will show result only for these specific problems', default=[])
    parser.add_argument('--problem-id', type=int, help='will show result only for this specific problem id')
    parser.add_argument('--dump-code', action='store_true', help='whether or not to download code for submissions. found in submissions folder')
    
    args = parser.parse_args()
    return args

def get_students(student_arg):
    if student_arg.endswith('.csv'):
        students = {}
        with open(student_arg, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                students[row['id']] = row['name']
        return students

    return {student_arg: 'Student'}

def filter_and_print_submission(submission, problem_prefix=None, problem_id=None, problems=None, token=None):
    problem = get_problem_info(submission['problem_id'], token)

    if problem_prefix and not problem['name'].startswith(problem_prefix):
        return None

    if problems and problem['name'] not in problems:
        return None

    if problem_id and problem['id'] != problem_id:
        return None

    print(f'\t{problem["name"]}: {submission["grade"]}')

    return problem

def dump_code(code, problem_name, student_name):
    if not os.path.exists('submissions'):
        os.makedirs('submissions')
    
    with open(f'submissions/{student_name}_{problem_name}.c', "w") as f:
        f.write(code)

def main(args):
    token = login()
    students = get_students(args.student)

    for student_id, student_name in students.items():
        print(f'Best submissions for student "{student_name}":')
        try:
            resp = requests.get(endpoints['submissions'], {'id': student_id}, auth=BearerAuth(token))
            resp.raise_for_status()
            
            submissions = resp.json()

            for submission in submissions:
                problem = filter_and_print_submission(submission, args.problem_prefix, args.problem_id, args.problems, token)
                
                if args.dump_code and problem:
                    dump_code(submission["code"], problem["name"], student_name)
            
        except requests.exceptions.HTTPError as error:
            print(resp.json())
            raise SystemExit(error)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        
    pass

if __name__ == '__main__':
    args = parse_args()
    main(args)
