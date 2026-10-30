Here is the complete system design, algorithm, Mermaid flowchart, and Python implementation for the **Student Timetable Conflict Detection System**.

---

### 1. Problem Statement

Educational institutions face complex scheduling challenges when assigning courses to specific classrooms, days, time slots, and instructors. Scheduling errors can lead to two major types of conflicts:

1. **Room Conflicts**: Two or more courses are assigned to the exact same physical room during overlapping time periods on the same day.
2. **Instructor / Schedule Conflicts**: An instructor (or student cohort) is assigned to teach/attend two different courses simultaneously during overlapping time slots.

The **Student Timetable Conflict Detection System** automates the validation of proposed timetables by parsing schedule strings and tuples, converting time blocks into comparable numerical intervals, detecting overlaps, identifying unavailable resources, and generating a detailed validation report.

---

### 2. Algorithm

1. **Define Representation**: Represent each class session as a tuple or structured object: `(course_code, room, day, start_time, end_time, instructor)`.
2. **Time Normalization**: Convert time strings (e.g., `"09:30"`) into minutes past midnight (e.g., $9 \times 60 + 30 = 570$ minutes) to enable precise mathematical comparisons.
3. **Interval Overlap Logic**: Two time intervals $[S_1, E_1]$ and $[S_2, E_2]$ on the same day overlap if and only if:

$$\max(S_1, S_2) < \min(E_1, E_2)$$


4. **Conflict Detection Pass**:
* **Room Overlap Check**: Group scheduled sessions by `(day, room)`. For each room on a given day, check every pair of courses for time overlaps.
* **Instructor Overlap Check**: Group scheduled sessions by `(day, instructor)`. Check for simultaneous overlapping bookings.


5. **Validation Result**: If any overlaps are found, flag the timetable as **Invalid** with descriptive error logs. If none are found, mark it as **Valid**.

---

### 3. Flowchart (Mermaid)

```mermaid
graph TD
    A[Start: Load Proposed Timetable Entries] --> B[Normalize Times into Minutes Past Midnight]
    B --> C{For Each Pair of Classes in Timetable}
    C --> D{Are Scheduled on the Same Day?}
    D -->|No| C
    D -->|Yes| E{Check Time Overlap:<br/>max(S1, S2) < min(E1, E2)}
    E -->|No Overlap| C
    E -->|Time Overlap Detected| F{Check Resource Shared}
    F -->|Same Room Assigned| G[Log Room Conflict Error]
    F -->|Same Instructor Assigned| H[Log Instructor Conflict Error]
    G --> C
    H --> C
    C -->|Processed All Pairs| I{Were Any Conflicts Found?}
    I -->|Yes| J[Mark Timetable as INVALID & Output Error Logs]
    I -->|No| K[Mark Timetable as VALID]
    J --> L[End]
    K --> L

```

---

### 4. Python Source Code

```python
class TimetableValidator:

    def __init__(self, timetable_entries):
        # Entry format: (course_code, room, day, start_time, end_time, instructor)
        # Times in 24-hour string format, e.g., "09:00", "11:30"
        self.entries = timetable_entries

    def _time_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def _check_overlap(self, start1, end1, start2, end2):
        s1 = self._time_to_minutes(start1)
        e1 = self._time_to_minutes(end1)
        s2 = self._time_to_minutes(start2)
        e2 = self._time_to_minutes(end2)

        # Overlap condition: max start < min end
        return max(s1, s2) < min(e1, e2)

    def validate_timetable(self):
        room_conflicts = []
        instructor_conflicts = []

        n = len(self.entries)
        for i in range(n):
            for j in range(i + 1, n):
                c1 = self.entries[i]
                c2 = self.entries[j]

                # Unpack fields
                code1, room1, day1, start1, end1, inst1 = c1
                code2, room2, day2, start2, end2, inst2 = c2

                # Only check if they occur on the same day
                if day1 == day2:
                    is_overlapping = self._time_to_minutes(
                        start1
                    ) < self._time_to_minutes(
                        end1
                    ) and self._check_overlap(
                        start1, end1, start2, end2
                    )

                    if is_overlapping:
                        # 1. Check Room Conflict
                        if room1 == room2:
                            room_conflicts.append(
                                f"Room '{room1}' is double-booked on {day1} between "
                                f"({start1}-{end1}) by {code1} and ({start2}-{end2}) by {code2}."
                            )

                        # 2. Check Instructor Conflict
                        if inst1 == inst2:
                            instructor_conflicts.append(
                                f"Instructor '{inst1}' is double-booked on {day1} between "
                                f"({start1}-{end1}) for {code1} and ({start2}-{end2}) for {code2}."
                            )

        is_valid = len(room_conflicts) == 0 and len(instructor_conflicts) == 0

        return {
            "is_valid": is_valid,
            "room_conflicts": room_conflicts,
            "instructor_conflicts": instructor_conflicts,
        }


# --- Sample Execution ---
if __name__ == "__main__":
    # Proposed Timetable Entries:
    # (Course Code, Room, Day, Start Time, End Time, Instructor)
    proposed_schedule = [
        ("CS101", "Auditorium A", "Monday", "09:00", "10:30", "Dr. Alan Turing"),
        (
            "MATH202",
            "Room 302",
            "Monday",
            "10:00",
            "11:30",
            "Dr. Katherine Johnson",
        ),  # Overlaps with CS101 time in a different room
        (
            "PHYS101",
            "Auditorium A",
            "Monday",
            "10:00",
            "11:00",
            "Dr. Richard Feynman",
        ),  # Room conflict with MATH202? No, MATH202 is in Room 302. But let's check Auditorium A vs CS101 (09:00-10:30 vs 10:00-11:00 -> Room conflict in Auditorium A!)
        (
            "CHEM101",
            "Lab 1",
            "Tuesday",
            "13:00",
            "15:00",
            "Dr. Alan Turing",
        ),  # Instructor conflict if he was teaching elsewhere, but Tuesday is fine.
    ]

    # Let's refine the sample list to trigger both room and instructor conflicts clearly:
    test_schedule = [
        ("CS101", "Hall 101", "Monday", "09:00", "10:30", "Dr. Alice"),
        (
            "MATH201",
            "Hall 101",
            "Monday",
            "10:00",
            "11:30",
            "Dr. Bob",
        ),  # ⚠️ Room Conflict in Hall 101 (09:00-10:30 & 10:00-11:30 overlap)
        (
            "PHYS301",
            "Lab 2",
            "Monday",
            "09:30",
            "11:00",
            "Dr. Alice",
        ),  # ⚠️ Instructor Conflict for Dr. Alice (teaching CS101 and PHYS301 at the same time)
    ]

    validator = TimetableValidator(test_schedule)
    result = validator.validate_timetable()

    print("=== TIMETABLE CONFLICT DETECTION REPORT ===")
    print(f"Proposed Timetable Status: {'VALID ✅' if result['is_valid'] else 'INVALID ❌'}\n")

    if not result["is_valid"]:
        print("--- ROOM CONFLICTS ---")
        if result["room_conflicts"]:
            for err in result["room_conflicts"]:
                print(f"  • {err}")
        else:
            print("  None.")

        print("\n--- INSTRUCTOR / FACULTY CONFLICTS ---")
        if result["instructor_conflicts"]:
            for err in result["instructor_conflicts"]:
                print(f"  • {err}")
        else:
            print("  None.")

```

---

### 5. Sample Input

```python
test_schedule = [
    ("CS101", "Hall 101", "Monday", "09:00", "10:30", "Dr. Alice"),
    ("MATH201", "Hall 101", "Monday", "10:00", "11:30", "Dr. Bob"),
    ("PHYS301", "Lab 2", "Monday", "09:30", "11:00", "Dr. Alice"),
]

```

---

### 6. Sample Output

```text
=== TIMETABLE CONFLICT DETECTION REPORT ===
Proposed Timetable Status: INVALID ❌

--- ROOM CONFLICTS ---
  • Room 'Hall 101' is double-booked on Monday between (09:00-10:30) by CS101 and (10:00-11:30) by MATH201.

--- INSTRUCTOR / FACULTY CONFLICTS ---
  • Instructor 'Dr. Alice' is double-booked on Monday between (09:00-10:30) for CS101 and (09:30-11:00) for PHYS301.

```
