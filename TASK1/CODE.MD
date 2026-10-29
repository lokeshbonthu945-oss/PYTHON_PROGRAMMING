# University Scholarship Allocation System Using Python

## 1. Problem Statement

The University Scholarship Allocation System is designed to identify eligible students based on their academic performance and financial background. The system collects each student's aggregate marks, subject-wise marks, attendance percentage, and annual family income.

Students who satisfy all the eligibility criteria are selected and ranked according to their aggregate marks. If two students have the same aggregate marks, ties are resolved using predefined rules:

1. Higher aggregate marks.
2. Higher attendance percentage.
3. Lower annual family income.
4. Alphabetical order of the student's name.

The system displays the eligible students in rank order and identifies students who do not meet the eligibility criteria.

Assumed eligibility criteria for this program:

- Aggregate marks: at least 75%.
- Minimum marks in every subject: 60%.
- Attendance: at least 75%.
- Annual family income: not more than ₹2,50,000.

These are sample rules for the program and can be changed according to university requirements.

## 2. Algorithm

1. Start the program.
2. Read the number of students.
3. Set the scholarship eligibility criteria.
4. For each student, input the name, aggregate marks, subject-wise marks, attendance, and annual family income.
5. Check whether the student satisfies all four eligibility criteria.
6. If eligible, add the student to the eligible list; otherwise, record the reason for rejection.
7. Sort eligible students by:
   - Aggregate marks in descending order.
   - Attendance in descending order.
   - Annual family income in ascending order.
   - Name in alphabetical order.
8. Assign ranks to the eligible students.
9. Display the eligible students with their ranks and the rejected students with their reasons.
10. Stop the program.

## 3. Flowchart 

```Mermaid
flowchart TD
    A([Start]) --> B[/Enter number of students/]
    B --> C[Set eligibility criteria]
    C --> D[/Enter student details and subject marks/]
    D --> E{Aggregate >= 75%?}
    E -- No --> R[Mark as not eligible]
    E -- Yes --> F{Every subject >= 60%?}
    F -- No --> R
    F -- Yes --> G{Attendance >= 75%?}
    G -- No --> R
    G -- Yes --> H{Annual income <= 250000?}
    H -- No --> R
    H -- Yes --> I[Add student to eligible list]
    R --> J{More students?}
    I --> J
    J -- Yes --> D
    J -- No --> K[Sort eligible students by tie-break rules]
    K --> L[Assign ranks]
    L --> M[/Display eligible ranking and rejection reasons/]
    M --> N([Stop])
```

## 5. Sample Input

```
Enter number of students: 4

Enter details of Student 1
Name: Anu
Aggregate marks (%): 90
Enter marks of 5 subjects: 90 85 92 88 95
Attendance (%): 92
Annual family income: 200000

Enter details of Student 2
Name: Ravi
Aggregate marks (%): 90
Enter marks of 5 subjects: 90 92 88 95 85
Attendance (%): 92
Annual family income: 180000

Enter details of Student 3
Name: Balu
Aggregate marks (%): 85
Enter marks of 5 subjects: 80 85 90 75 95
Attendance (%): 95
Annual family income: 150000

Enter details of Student 4
Name: Chitra
Aggregate marks (%): 80
Enter marks of 5 subjects: 80 55 85 90 90
Attendance (%): 80
Annual family income: 200000
```

## 6. Sample Output

```
--- ELIGIBLE STUDENTS ---
Rank  Name       Aggregate  Attendance  Income
1     Ravi       90.0       92.0        Rs.180000
2     Anu        90.0       92.0        Rs.200000
3     Balu       85.0       95.0        Rs.150000

--- REJECTED STUDENTS ---
Chitra: Subject marks below 60% or invalid count
```

