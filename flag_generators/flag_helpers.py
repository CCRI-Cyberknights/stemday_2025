import random
import string
import re

class FlagUtils:
    """
    Utility class for flag generation and validation.
    """
    @classmethod
    def generate_real_flag(cls) -> str:
        """
        Generate a valid CCRI flag: CCRI-ABCD-1234
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=4))
        digits = ''.join(random.choices(string.digits, k=4))
        return f"CCRI-{letters}-{digits}"

    @classmethod
    def generate_fake_flag(cls) -> str:
        """
        Generate an invalid flag in one of two strict fake formats.
        **NOTE: Fake flags must NOT begin with CCRI-**
        """
        while True:
            letters1 = ''.join(random.choices(string.ascii_uppercase, k=4))
            letters2 = ''.join(random.choices(string.ascii_uppercase, k=4))
            digits = ''.join(random.choices(string.digits, k=4))
            format_choice = random.choice([1, 2])

            if format_choice == 1:
                fake = f"{letters1}-{letters2}-{digits}"  # AAAA-BBBB-1111
            else:
                fake = f"{letters1}-{digits}-{letters2}"  # AAAA-1111-BBBB

            # Ensure no fake flag ever starts with CCRI
            if not fake.startswith("CCRI"):
                return fake

    @staticmethod
    def validate_flag_format(flag: str) -> bool:
        """
        Validate flag format: CCRI-XXXX-1234
        """
        return bool(re.match(r"^CCRI-[A-Z]{4}-\d{4}$", flag))