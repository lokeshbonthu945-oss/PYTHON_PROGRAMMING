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
