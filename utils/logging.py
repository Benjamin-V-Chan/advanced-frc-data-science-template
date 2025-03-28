import datetime
import logging

# ===========================================
# LOGGING CONFIGURATION
# ===========================================

logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ===========================================
# SECTIONING AND FORMATTING FUNCTIONS
# ===========================================

def log_bar(character="=", length=80):
    """Prints a separation bar with customizable characters and length."""
    print(character * length)

def log_header(title, symbol="-", padding=4):
    """Prints a formatted section header with a title."""
    title = f" {title} "
    print(symbol * padding + title + symbol * (80 - len(title) - padding))
    logging.info(f"[SECTION] {title.strip()}")

def log_subheader(subtitle, symbol="~", padding=2):
    """Logs a formatted sub-heading with a subtitle."""
    subtitle = f" {subtitle} "
    print(symbol * padding + subtitle + symbol * (80 - len(subtitle) - padding))
    logging.info(f"[SUB-SECTION] {subtitle.strip()}")

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

# ===========================================
# CORE LOGGING FUNCTIONS
# ===========================================

def log_info(message):
    """Logs an informational message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[INFO] {message} - {timestamp}"
    print(log_message)
    logging.info(message)

def log_warning(
    message,
    function_name="N/A",
    issue_type="N/A",
    location="N/A",
    code=None
):
    """
    Logs a warning message with standardized bracket labels.

    :param message:        The core description of what’s wrong.
    :param function_name:  Name of the function or context calling the warning.
    :param issue_type:     Short string for the issue category (e.g. 'missing_key').
    :param location:       Data path or field that triggered the warning (e.g. 'metadata.someKey').
    :param code:           Optional short code for reference (e.g. 'W101').
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build bracket labels
    log_prefix = "[WARNING"
    if code:
        log_prefix += f" {code}"
    log_prefix += "]"

    if function_name != "N/A":
        log_prefix += f" [function={function_name}]"
    if issue_type != "N/A":
        log_prefix += f" [issue={issue_type}]"
    if location != "N/A":
        log_prefix += f" [location={location}]"

    # Combine everything
    log_message = f"{log_prefix} {message} - {timestamp}"
    print(log_message)
    logging.warning(log_message)

def log_success(message):
    """Logs a success message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[SUCCESS] {message} - {timestamp}"
    print(log_message)
    logging.info(message)

# ===========================================
# HELPER WARNING FUNCTIONS
# ===========================================

def warn_missing_key(
    key_name,
    function_name="N/A",
    location="N/A",
    code=None
):
    """
    Warn that a required key is missing.
    """
    message = f"Missing required key '{key_name}'."
    log_warning(
        message=message,
        function_name=function_name,
        issue_type="missing_key",
        location=location,
        code=code
    )


def warn_invalid_type(
    key_or_field,
    expected_type,
    actual_value,
    function_name="N/A",
    location="N/A",
    code=None
):
    """
    Warn that a field has an invalid type compared to the expected type.
    Shows both the type and actual value.
    """
    actual_type = type(actual_value).__name__
    message = (
        f"'{key_or_field}' should be '{expected_type}', "
        f"but got type '{actual_type}' with value '{actual_value}'."
    )
    log_warning(
        message=message,
        function_name=function_name,
        issue_type="invalid_type",
        location=location,
        code=code
    )


def warn_invalid_value(
    key_or_field,
    expected_condition,
    actual_value,
    function_name="N/A",
    location="N/A",
    code=None
):
    """
    Warn that a field's value is invalid given some expected condition.
    Shows the actual value and its type as well.
    """
    actual_type = type(actual_value).__name__
    message = (
        f"'{key_or_field}' is invalid. Expected {expected_condition}, "
        f"but got type '{actual_type}' with value '{actual_value}'."
    )
    log_warning(
        message=message,
        function_name=function_name,
        issue_type="invalid_value",
        location=location,
        code=code
    )


def warn_duplicate_value(
    key_or_field,
    actual_values=None,
    function_name="N/A",
    location="N/A",
    code=None
):
    """
    Warn that duplicates were found where uniqueness was required.
    Optionally show the entire list or duplicates.
    """
    message = f"'{key_or_field}' contains duplicate values."
    if actual_values is not None:
        message += f" Received values: {actual_values}"

    log_warning(
        message=message,
        function_name=function_name,
        issue_type="duplicate_value",
        location=location,
        code=code
    )


def warn_out_of_range(
    key_or_field,
    range_description,
    actual_value,
    function_name="N/A",
    location="N/A",
    code=None
):
    """
    Warn that a numerical field is out of a given range.
    Shows the actual value and its type.
    """
    actual_type = type(actual_value).__name__
    message = (
        f"'{key_or_field}' is out of range. Expected {range_description}, "
        f"but got type '{actual_type}' with value '{actual_value}'."
    )
    log_warning(
        message=message,
        function_name=function_name,
        issue_type="out_of_range",
        location=location,
        code=code
    )