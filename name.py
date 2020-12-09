import spacy
from profanity_filter import ProfanityFilter
from username_validator import UsernameValidator, PROTOCOL_HOSTNAMES, SENSITIVE_FILENAMES

nlp = spacy.load('en')
reserved = (PROTOCOL_HOSTNAMES + SENSITIVE_FILENAMES)

profanity_filter = ProfanityFilter(nlps={ "en": nlp })
nlp.add_pipe(profanity_filter.spacy_component, last=True)

class Checker:
    def __init__(self, username_str: str):
        try:
            UsernameValidator(additional_names=["ommc"], reserved_names=reserved).validate_all(username_str)
            self.is_valid = nlp(username_str)._.is_profane
        except Exception:
            self.is_valid = False
