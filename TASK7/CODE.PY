import math


class AttendanceRecoverySystem:

    def __init__(self, target_percentage=75.0):
        self.target_percentage = target_percentage

    def analyze_attendance(self, total_held, total_attended):
        if total_held <= 0:
            raise ValueError("Total classes held must be greater than zero.")
        if total_attended > total_held:
            raise ValueError("Attended classes cannot exceed total classes held.")

        current_percentage = (total_attended / total_held) * 100.0
        target_ratio = self.target_percentage / 100.0

        result = {
            "total_held": total_held,
            "total_attended": total_attended,
            "current_percentage": round(current_percentage, 2),
            "target_percentage": self.target_percentage,
        }

        if current_percentage >= self.target_percentage:
            # Already eligible, calculate how many can be safely missed
            # Formula: (Attended - Target_Ratio * Held) / Target_Ratio
            safe_misses = math.floor(
                (total_attended - (target_ratio * total_held)) / target_ratio
            )
            result["status"] = "ELIGIBLE (Above Target)"
            result["safe_misses_allowed"] = max(0, safe_misses)
            result["message"] = (
                f"You are safe! You can miss up to {max(0, safe_misses)} upcoming classes "
                f"and still maintain at least {self.target_percentage}% attendance."
            )
        else:
            # Shortage, calculate minimum consecutive classes needed
            # Formula: ceil( (Target_Ratio * Held - Attended) / (1 - Target_Ratio) )
            numerator = (target_ratio * total_held) - total_attended
            denominator = 1.0 - target_ratio
            classes_needed = math.ceil(numerator / denominator)

            result["status"] = "SHORTAGE (Recovery Required)"
            result["classes_needed_consecutive"] = classes_needed
            result["message"] = (
                f"Attendance shortfall detected. You must attend the next "
                f"{classes_needed} consecutive classes without missing any "
                f"to reach the {self.target_percentage}% threshold."
            )

        return result


# --- Sample Execution ---
if __name__ == "__main__":
    system = AttendanceRecoverySystem(target_percentage=75.0)

    # Test Scenarios
    scenarios = [
        {"name": "Student A (Shortage)", "held": 40, "attended": 26},  # 65.0%
        {
            "name": "Student B (Borderline/Safe)",
            "held": 50,
            "attended": 39,
        },  # 78.0%
        {"name": "Student C (Critical Shortage)", "held": 60, "attended": 35},  # 58.33%
    ]

    print("=== ATTENDANCE RECOVERY & STATUS ANALYSIS ===\n")
    for student in scenarios:
        report = system.analyze_attendance(student["held"], student["attended"])
        print(f"--- {student['name']} ---")
        print(f"Classes Held: {report['total_held']} | Attended: {report['total_attended']}")
        print(f"Current Attendance: {report['current_percentage']}%")
        print(f"Status: {report['status']}")
        print(f"Action Guide: {report['message']}\n")
