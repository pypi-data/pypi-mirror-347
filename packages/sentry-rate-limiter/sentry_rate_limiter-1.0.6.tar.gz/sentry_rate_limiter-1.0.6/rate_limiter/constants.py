PII_REGEX_PATTERNS = {
    "email": r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",
    "phone": r"(\+\d{1,3}[- ]?)?\d{10}[\s , )]",
    "phone2": r"(?:\+?\d{1,3}|0)?([6-9]\d{9})\b",
    "pan": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "aadhar": r"[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[" " , . )]",
    "recording_url": str(r'[https?: // " ]\S+\.mp3[ \ {t1} . , " ]?'.format(t1="'")),
}

# Set of Exception Classes to exclude
EXCLUDE_EXCEPTION_CLASSES = set()

# List of Exception messages prefix to exclude
EXCLUDE_EXCEPTION_MSG_PREFIXES = []

# Dictionary of logger and list of corresponding prefix messages to silence
SILENCED_LOGGER_MESSAGES = {
    "elasticapm.transport": ["Failed to submit message", "Unable to reach APM Server"]
}

RESTRICTED_PROPAGATION_SERIES = {1, 2, 4, 8, 16, 32, 64, 128, 256}
STANDARD_PROPAGATION_SERIES = {1, 2, 3, 4, 9, 16, 25, 36, 49}

