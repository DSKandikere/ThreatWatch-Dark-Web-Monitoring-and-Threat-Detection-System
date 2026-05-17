# core/parser.py

import re

class DataParser:

    def __init__(self):
        self.email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
        self.password_pattern = r"password[:=]\s*\S+"
        self.credit_card_pattern = r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"

    def extract_emails(self, text):
        return re.findall(self.email_pattern, text)

    def extract_passwords(self, text):
        return re.findall(self.password_pattern, text)

    def extract_credit_cards(self, text):
        return re.findall(self.credit_card_pattern, text)

    def parse_all(self, text):
        return {
            "emails": self.extract_emails(text),
            "passwords": self.extract_passwords(text),
            "credit_cards": self.extract_credit_cards(text)
        }
