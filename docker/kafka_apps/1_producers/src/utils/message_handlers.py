import logging

class SuccessHandler:

  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def __call__(self, record_metadata):
    self.logger.info(f"Topic {record_metadata.topic()};Partition {record_metadata.partition()};Offset {record_metadata.offset()}")
    

class ErrorHandler:

  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def __call__(self, error):
    self.logger.error(f"Error: {error}")