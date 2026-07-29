import re
import pandas as pd


def read_log_file(uploaded_file):
    """
    Returns raw log lines.
    """
    uploaded_file.seek(0)
    return uploaded_file.read().decode("utf-8").splitlines()


def parse_log_file(uploaded_file):
    """
    Converts Spring Boot logs into a DataFrame.
    """

    uploaded_file.seek(0)

    lines = uploaded_file.read().decode("utf-8").splitlines()

    pattern = re.compile(
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+'
        r'(?P<level>\w+)\s+'
        r'\[(?P<thread>.*?)\]\s+'
        r'(?P<logger>.*?)\s*:\s*'
        r'(?P<message>.*)'
    )

    records = []

    for line in lines:
        match = pattern.match(line)

        if match:
            records.append(match.groupdict())

    return pd.DataFrame(records)