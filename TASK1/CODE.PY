
# University Scholarship Allocation System

students = []
eligible_students = []
rejected_students = []

n = int(input("Enter number of students: "))

for i in range(n):
    print("\nEnter details of Student", i + 1)

    name = input("Name: ")
    aggregate = float(input("Aggregate marks (%): "))
    subjects = list(map(float, input(
        "Enter marks of 5 subjects: "
    ).split()))
    attendance = float(input("Attendance (%): "))
    income = float(input("Annual family income: "))

    student = {
        "name": name,
        "aggregate": aggregate,
        "subjects": subjects,
        "attendance": attendance,
        "income": income
    }

    reasons = []

    if aggregate < 75:
        reasons.append("Aggregate below 75%")

    if len(subjects) != 5 or any(mark < 60 for mark in subjects):
        reasons.append("Subject marks below 60% or invalid count")

    if attendance < 75:
        reasons.append("Attendance below 75%")

    if income > 250000:
        reasons.append("Income exceeds Rs. 250000")

    if reasons:
        rejected_students.append((name, reasons))
    else:
        eligible_students.append(student)

# Sort by aggregate, attendance, income, and name
eligible_students.sort(
    key=lambda s: (
        -s["aggregate"],
        -s["attendance"],
        s["income"],
        s["name"].lower()
    )
)

print("\n--- ELIGIBLE STUDENTS ---")

if eligible_students:
    print("Rank  Name       Aggregate  Attendance  Income")

    for rank, s in enumerate(eligible_students, start=1):
        print(
            f"{rank:<5} {s['name']:<10} "
            f"{s['aggregate']:<10.1f} "
            f"{s['attendance']:<11.1f} "
            f"Rs.{s['income']:.0f}"
        )
else:
    print("No eligible students.")

print("\n--- REJECTED STUDENTS ---")

if rejected_students:
    for name, reasons in rejected_students:
        print(name + ": " + ", ".join(reasons))
else:
    print("No rejected students.")

