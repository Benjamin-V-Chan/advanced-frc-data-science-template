import datetime
import logging

# Configure logging
logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Sectioning and Formatting Functions
def log_bar(character="=", length=80):
    """Prints a separation bar with customizable characters and length."""
    print(character * length)

def log_header(title, symbol="-", padding=4):
    """Prints a formatted section header with a title."""
    title = f" {title} "
    print(symbol * padding + title + symbol * (80 - len(title) - padding))
    logging.info(f"[SECTION] {title.strip()}")

def script_start(script_name="Script Execution Started"):
    """Logs and displays the script start with a header and timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_bar("=")
    print(f"[START] {script_name} - {timestamp}")
    log_bar("=")
    logging.info(f"[START] {script_name} - {timestamp}")

def script_end(script_name="Script Execution Finished"):
    """Logs and displays the script end with a header and timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_bar("=")
    print(f"[END] {script_name} - {timestamp}")
    log_bar("=")
    logging.info(f"[END] {script_name} - {timestamp}")
    
# Logging Functions
def log_info(message):
    """Logs an informational message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[INFO] {message} - {timestamp}"
    print(log_message)
    logging.info(message)

def log_warning(message):
    """Logs a warning message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[WARNING] {message} - {timestamp}"
    print(log_message)
    logging.warning(message)

def log_success(message):
    """Logs a success message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[SUCCESS] {message} - {timestamp}"
    print(log_message)
    logging.info(message)