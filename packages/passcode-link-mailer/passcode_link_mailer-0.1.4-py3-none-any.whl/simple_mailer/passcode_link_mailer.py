import smtplib
import secrets
import threading
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # For path operations
from pathlib import Path  # For robust path handling


class EmailSendingError(Exception):
    """Base exception for email sending failures in PasscodeLinkMailer."""
    pass


class EmailSendingAuthError(EmailSendingError):
    """Raised for authentication failures during email sending."""
    pass


class EmailSendingConnectionError(EmailSendingError):
    """Raised for connection failures during email sending."""
    pass


class PasscodeLinkMailer:
    """
    A class to handle sending email confirmations with a unique passcode and a timed link,
    primarily designed for use with Gmail using an App Password.
    It supports different email styling options loaded from external HTML files.
    """

    def __init__(self, sender_email: str, gmail_app_password: str, subject: str,
                 message_body_template: str, valid_for_duration_seconds: int, confirmation_link_base: str,
                 email_style: str = 'standard', templates_dir: str = None):
        """
        Initializes the PasscodeLinkMailer service.

        Args:
            sender_email (str): The Gmail address from which emails will be sent.
            gmail_app_password (str): The 16-character App Password generated from Gmail.
            subject (str): The subject line for the confirmation email. Can contain placeholders
                           like {recipient_email} or {passcode}.
            message_body_template (str): The main content of the email that you provide.
                                         You can use placeholders like {recipient_email}, {passcode},
                                         {validity_duration}, and {full_confirmation_link}.
            valid_for_duration_seconds (int): How long the generated passcode and link should be
                                             considered valid, in seconds.
            confirmation_link_base (str): The base URL for the confirmation link.
                                          The passcode will be appended as a query parameter.
            email_style (str, optional): The style of the email template to use. Options are:
                                        'standard' (default), 'minimal', or 'modern'.
            templates_dir (str, optional): The directory where HTML email templates are stored.
                                           If None, defaults to a 'templates' subdirectory
                                           within the same directory as this file.
        """
        if not sender_email or "@" not in sender_email:
            raise ValueError("A valid sender_email is required.")
        if not gmail_app_password:
            raise ValueError("gmail_app_password is required and cannot be empty.")

        valid_styles = ['standard', 'minimal', 'modern']
        if email_style not in valid_styles:
            raise ValueError(f"Invalid email_style. Choose from: {', '.join(valid_styles)}")

        self.sender_email = sender_email
        self.gmail_app_password = gmail_app_password
        self.subject_template = subject
        self.message_body_template = message_body_template  # User's specific message part
        self.valid_for_duration_seconds = valid_for_duration_seconds
        self.confirmation_link_base = confirmation_link_base.rstrip('/')
        self.email_style = email_style

        if templates_dir is None:
            # Default to a 'templates' subdirectory relative to this file's location
            base_path = Path(__file__).parent
            self.templates_dir = base_path / 'templates'
        else:
            self.templates_dir = Path(templates_dir)

        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def _generate_passcode(self, length: int = 24) -> str:
        """Generates a cryptographically strong, URL-safe passcode."""
        return secrets.token_urlsafe(length)

    def _format_duration(self, seconds: int) -> str:
        """Formats seconds into a user-friendly string."""
        if seconds < 0:
            return "an invalid duration"
        if seconds < 60:
            return f"{seconds} second{'s' if seconds != 1 else ''}"

        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minute{'s' if minutes != 1 else ''}"

        hours = minutes // 60
        remaining_minutes = minutes % 60

        if remaining_minutes > 0:
            return f"{hours} hour{'s' if hours != 1 else ''} and {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
        return f"{hours} hour{'s' if hours != 1 else ''}"

    def _load_template(self, template_name: str) -> str:
        """Loads an HTML template from the templates directory."""
        template_file = self.templates_dir / template_name
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Email template '{template_file}' not found. Ensure it's in the templates directory and the directory is included in your package data.")
        except Exception as e:
            raise Exception(f"Error loading email template '{template_file}': {e}")

    def _create_html_email_body(self, recipient_email: str, passcode: str, full_confirmation_link: str) -> str:
        """
        Creates the HTML body for the confirmation email by loading a template
        and formatting it with the necessary data.
        """
        validity_str = self._format_duration(self.valid_for_duration_seconds)
        current_year = time.strftime('%Y')  # Still generated, but templates might not use it

        personalized_message_body = self.message_body_template.format(
            recipient_email=recipient_email,
            passcode=passcode,
            validity_duration=validity_str,
            full_confirmation_link=full_confirmation_link
        )

        if self.email_style == 'minimal':
            template_filename = 'minimal_template.html'
        elif self.email_style == 'modern':
            template_filename = 'modern_template.html'
        else:
            template_filename = 'standard_template.html'

        base_html_template = self._load_template(template_filename)

        final_html = base_html_template.format(
            personalized_message_body=personalized_message_body,
            passcode=passcode,
            full_confirmation_link=full_confirmation_link,
            validity_str=validity_str,
            current_year=current_year  # Pass it in case a template still uses it
        )
        return final_html

    def _send_email_worker(self, recipient_email: str, subject: str, html_body: str):
        """The actual worker function that sends the email."""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender_email, self.gmail_app_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
        except smtplib.SMTPAuthenticationError as e:
            error_message = f"SMTP Authentication Error for {self.sender_email}: {e}. Ensure App Password is correct and 2FA is enabled."
            raise EmailSendingAuthError(error_message) from e
        except smtplib.SMTPConnectError as e:
            error_message = f"SMTP Connection Error: Could not connect to {self.smtp_server}:{self.smtp_port}. {e}"
            raise EmailSendingConnectionError(error_message) from e
        except smtplib.SMTPServerDisconnected as e:
            error_message = f"SMTP Server Disconnected: {e}. This might be a temporary issue."
            raise EmailSendingConnectionError(error_message) from e
        except smtplib.SMTPException as e:
            error_message = f"An SMTP error occurred while sending email to {recipient_email}: {e}"
            raise EmailSendingError(error_message) from e
        except Exception as e:
            error_message = f"An unexpected error occurred in _send_email_worker for {recipient_email}: {e}"
            raise EmailSendingError(error_message) from e

    def send(self, recipient_email: str, delay_seconds: int = 0) -> str:
        """
        Generates a passcode, prepares the confirmation email, and sends it
        after an optional delay using a daemon thread.
        """
        if not recipient_email or "@" not in recipient_email:
            raise ValueError("A valid recipient_email is required.")

        passcode = self._generate_passcode()

        separator = '&' if '?' in self.confirmation_link_base else '?'
        full_confirmation_link = f"{self.confirmation_link_base}{separator}passcode={passcode}"

        validity_str = self._format_duration(self.valid_for_duration_seconds)

        format_vars_for_subject = {
            'recipient_email': recipient_email,
            'passcode': passcode,
            'validity_duration': validity_str,
            'full_confirmation_link': full_confirmation_link
        }

        try:
            final_subject = self.subject_template.format(**format_vars_for_subject)
        except KeyError:
            final_subject = self.subject_template

        html_body = self._create_html_email_body(recipient_email, passcode, full_confirmation_link)

        if delay_seconds > 0:
            email_thread = threading.Thread(
                target=self._delayed_send,
                args=(delay_seconds, recipient_email, final_subject, html_body),
                daemon=True
            )
            email_thread.start()
        else:
            self._send_email_worker(recipient_email, final_subject, html_body)

        return passcode

    def _delayed_send(self, delay_seconds: int, recipient_email: str, subject: str, html_body: str):
        """Helper function to handle the delay before calling _send_email_worker."""
        try:
            time.sleep(delay_seconds)
            self._send_email_worker(recipient_email, subject, html_body)
        except EmailSendingError as e:
            print(f"Error sending email in delayed thread to {recipient_email}: {e}")
        except Exception as e:
            print(f"Unexpected error in delayed send thread for {recipient_email}: {e}")
