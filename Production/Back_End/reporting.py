"""
Provides issue reporting services
Email is the highest level of reporting
File is the second highest level of reporting
Printing is the lowest level of reporting
"""
# Sending Messages
from smtplib import SMTP

# Dating Messages
from datetime import datetime

def send_email(message):
    """
    Send email to administrator
    """
    # Details of email
    send_to = "kevin.chu215@gmail.com"
    email = "financialanalysis21842@gmail.com"
    password = "?continue=https://myaccount.google.com/u/1/personal-info&rapt=AEjHL4MwSL1"

    try:
        # Creating email client
        smtp = SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(email, password)

        # Sending email
        smtp.sendmail(email, send_to, message)

        # Closinge mail client
        smtp.quit()
    except Exception as e:
        # Log issue from failed email
        log_issue("reporting_stack", f"{message}\t{e}")

def log_issue(file, message, date=True, new_line=True):
    """
    Write issue to a file
    """
    try:
        # Attempt to write issue to file
        with open(f"{file}.txt", "ab") as fp:
            if date is True:
                # Writing desired message along with a timestamp
                message = f"{message}\t{datetime.utcnow()}"

            if new_line is True:
                # Writing desired message along with a new line
                message = f"{message}\n"

            # Writing message
            fp.write(message.encode("utf8"))
    except Exception as e:
        # Print issue to terminal along with a timestamp
        print_issue(f"Error trying to write ({message}) to ({file}.txt)\t{e}")

def print_issue(message):
    """
    Prints issue message to terminal
    """
    print(f"({message}) at {datetime.utcnow()}")
