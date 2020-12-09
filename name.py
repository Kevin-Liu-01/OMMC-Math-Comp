from profanityfilter import ProfanityFilter
from username_validator import UsernameValidator, PROTOCOL_HOSTNAMES, SENSITIVE_FILENAMES

reserved = (PROTOCOL_HOSTNAMES + SENSITIVE_FILENAMES)
filter = ProfanityFilter()

class Checker:
    def __init__(self, username_str: str):
        if " " in username_str:
            self.is_valid = False
            return

        try:
            UsernameValidator(additional_names=["ommc"], reserved_names=reserved).validate_all(username_str)
            self.is_valid = filter.is_clean(username_str) and not filter.is_profane(username_str)
        except Exception:
            self.is_valid = False
