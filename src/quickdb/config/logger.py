import logging
# Configure the logger
logger = logging.getLogger("application_logger")
logger.setLevel(logging.DEBUG)  # Set the log level to Debug

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define log format
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Usage example:
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
