import logging
from typing import Any


class SuccessHandler:

    def __init__(self, person):
        self.person = person

    def __call__(self, rec_metadata) -> Any:
        logging.info(f"Message of person {self.person} successfully sent to topic {rec_metadata.topic} at partition {rec_metadata.partition} with offset {rec_metadata.offset}")

class ErrorHandler:
    
    def __init__(self, person):
        self.person = person

    def __call__(self, exc) -> Any:
        logging.error(f"Error while sending message of person {self.person}: {exc}")