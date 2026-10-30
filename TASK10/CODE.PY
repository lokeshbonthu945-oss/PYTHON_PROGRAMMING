import re


class PasswordPolicyEngine:

    def __init__(self, min_length=10, prohibited_words=None):
        self.min_length = min_length
        self.prohibited_words = prohibited_words or [
            "password",
            "12345",
            "qwerty",
            "admin",
            "welcome",
            "letmein",
        ]

    def validate_password(self, password):
        failures = []

        # 1. Minimum Length Check
        if len(password) < self.min_length:
            failures.append(
                f"Password is too short (Length: {len(password)}). Must be at least {self.min_length} characters."
            )

        # 2. Character Category Checks
        if not re.search(r"[A-Z]", password):
            failures.append(
                "Missing uppercase letter (Requires at least one A-Z)."
            )
        if not re.search(r"[a-z]", password):
            failures.append(
                "Missing lowercase letter (Requires at least one a-z)."
            )
        if not re.search(r"[0-9]", password):
            failures.append("Missing numeric digit (Requires at least one 0-9).")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            failures.append(
                "Missing special character (Requires at least one symbol like !@#$)."
            )

        # 3. Consecutive Character Repetition Check (e.g., 'aaa')
        if re.search(r"(.)\1{2,}", password):
            failures.append(
                "Contains excessive consecutive character repetitions (e.g., 'aaa' is not allowed)."
            )

        # 4. Prohibited Substrings Check (Case-insensitive)
        lower_pass = password.lower()
        for word in self.prohibited_words:
            if word in lower_pass:
                failures.append(
                    f"Contains prohibited weak word or pattern ('{word}')."
                )
                break  # Log once for blacklist

        is_valid = len(failures) == 0

        return {
            "password": (
                "*" * len(password) if password else ""
            ),  # Masked for security in logs
            "is_valid": is_valid,
            "failure_reasons": failures,
        }


# --- Sample Execution ---
if __name__ == "__main__":
    validator = PasswordPolicyEngine(min_length=10)

    test_passwords = [
        "SecureP@ss2026",  # Strong, valid password
        "short",  # Too short, missing categories
        "Password123!",  # Contains prohibited word 'password' & number sequence '123'
        "NoSpecialChar1",  # Missing special character
        "Excellênt###aaa",  # Contains 'aaa' repetition
    ]

    print("=== PASSWORD POLICY VALIDATION ENGINE REPORT ===")
    for pwd in test_passwords:
        result = validator.validate_password(pwd)
        print(f"\nEvaluating Password: '{pwd}'")
        print(
            f"Status: {'VALID ✅' if result['is_valid'] else 'INVALID ❌'}"
        )

        if not result["is_valid"]:
            print("  Failure Reasons:")
            for reason in result["failure_reasons"]:
                print(f"    • {reason}")
        else:
            print("  Success: Password meets all security requirements.")
