# LambdaChecker Grading Helper
Features:
- Login with a teacher account with the correct API permissions
- Input a single student id or a .csv file containing multiple students
- See scores of students in an easier mannner
- Get each submission's code for manual review

Usage:
```
usage: grade.py [-h] [--problem-prefix PROBLEM_PREFIX] [--problems [PROBLEMS [PROBLEMS ...]]] [--problem-id PROBLEM_ID] [--dump-code] student

Helper CLI tool for easier grading of lambdachecker students.

positional arguments:
  student               id of student on lambdachecker or path to .csv file containing students

optional arguments:
  -h, --help            show this help message and exit
  --problem-prefix PROBLEM_PREFIX
                        will show problems only if they have this prefix
  --problems [PROBLEMS [PROBLEMS ...]]
                        will show result only for these specific problems
  --problem-id PROBLEM_ID
                        will show result only for this specific problem id
  --dump-code           whether or not to download code for submissions. found in submissions folder
```

Sample Output:
```
./grade.py students.csv --problems Circles "LinkedList Implementation" "Hashmap Implementation" --dump-code
Best submissions for student "Student 1":
        Circles: 100.0
        LinkedList Implementation: 100.0
        Hashmap Implementation: 100.0
Best submissions for student "Student 2":
        Circles: 100.0
        LinkedList Implementation: 100.0
Best submissions for student "Student 3":
        Circles: 100.0
        LinkedList Implementation: 100.0
```

.csv file used:
```
id,name
484,Student 1
436,Student 2
518,Student 3
```

Generated submissions structure:
```
.
└── submissions
    ├── Student 1_Circles.c
    ├── Student 1_Hashmap Implementation.c
    ├── Student 1_LinkedList Implementation.c
    ├── Student 2_Circles.c
    ├── Student 2_LinkedList Implementation.c
    ├── Student 3_Circles.c
    └── Student 3_LinkedList Implementation.c
```

### Examples
  - Check score of student with id 484 for problems Circles and Hashmap Implementation: `./grade.py 484 --problems Circles "Hashmap Implementation"`
  - Read students from a csv file, check their scores for problem Circles and also download their code: `./grade.py students.csv --problems Circles --dump-code`

### FAQs
- How can my students know their lambdachecker Id?
    - **Step 1.** Go to lambdachecker and login
    - **Step 2.** Press F12 to open DevTools
    - **Step 3.** Go to the Console tab
    - **Step 4.** Paste the following code: `console.log(localStorage.getItem("userId"));`
    - **Step 5.** Press enter, id should appear in console
    - **Step 6.** Profit