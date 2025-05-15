import smtplib
import secrets
import threading
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    """

    def __init__(self, sender_email: str, gmail_app_password: str, subject: str,
                 message_body_template: str, valid_for_duration_seconds: int, confirmation_link_base: str):
        """
        Initializes the PasscodeLinkMailer service.

        Args:
            sender_email (str): The Gmail address from which emails will be sent.
            gmail_app_password (str): The 16-character App Password generated from Gmail.
            subject (str): The subject line for the confirmation email. Can contain placeholders
                           like {recipient_email} or {passcode}.
            message_body_template (str): The main content of the email before the confirmation link/button.
                                         You can use placeholders like {recipient_email}, {passcode},
                                         and {validity_duration} which will be replaced.
            valid_for_duration_seconds (int): How long the generated passcode and link should be
                                             considered valid, in seconds.
            confirmation_link_base (str): The base URL for the confirmation link.
                                          The passcode will be appended like:
                                          'http://yourdomain.com/confirm?passcode=GENERATED_PASSCODE'
        """
        if not sender_email or "@" not in sender_email:
            raise ValueError("A valid sender_email is required.")
        if not gmail_app_password:
            raise ValueError("gmail_app_password is required and cannot be empty.")

        self.sender_email = sender_email
        self.gmail_app_password = gmail_app_password
        self.subject_template = subject
        self.message_body_template = message_body_template
        self.valid_for_duration_seconds = valid_for_duration_seconds
        self.confirmation_link_base = confirmation_link_base.rstrip('/')

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

    def _create_html_email_body(self, recipient_email: str, passcode: str, full_confirmation_link: str) -> str:
        """Creates the HTML body for the confirmation email."""
        validity_str = self._format_duration(self.valid_for_duration_seconds)

        personalized_message_body = self.message_body_template.format(
            recipient_email=recipient_email,
            passcode=passcode,
            validity_duration=validity_str,
            full_confirmation_link=full_confirmation_link
        )

        # Enhanced HTML styling for a more professional look
        html_content = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f7f6; }}
                    .email-wrapper {{ width: 100%; background-color: #f4f7f6; padding: 20px 0; }}
                    .email-container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); overflow: hidden; }}
                    .header {{ text-align: center; padding: 30px 20px; background-color: #007bff; color: #ffffff; }}
                    .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
                    .content {{ padding: 30px 25px; }}
                    .content p {{ margin-bottom: 18px; font-size: 16px; }}
                    .button-container {{ text-align: center; margin: 30px 0; }}
                    .button {{
                        display: inline-block;
                        padding: 14px 30px;
                        font-size: 16px;
                        font-weight: 500;
                        color: #ffffff !important;
                        background-color: #007bff;
                        text-decoration: none;
                        border-radius: 5px;
                        transition: background-color 0.2s ease-in-out, transform 0.1s ease;
                    }}
                    .button:hover {{ background-color: #0056b3; transform: translateY(-1px); }}
                    .link-fallback {{ margin-top: 20px; text-align: center; font-size: 0.9em; }}
                    .link-fallback p {{ margin-bottom: 5px; }}
                    .link-fallback a {{ color: #007bff; text-decoration: none; }}
                    .link-fallback a:hover {{ text-decoration: underline; }}
                    .passcode-info {{ font-size: 0.95em; color: #444444; margin-top: 25px; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px; }}
                    .passcode-info strong {{ color: #0056b3; }}
                    .footer {{ font-size: 0.8em; color: #888888; margin-top: 30px; text-align: center; border-top: 1px solid #e0e0e0; padding: 20px 25px; }}
                    .footer p {{ margin-bottom: 5px; }}
                </style>
            </head>
            <body>
                <div class="email-wrapper">
                    <div class="email-container">
                        <div class="header">
                            <h1>Confirmation Required</h1>
                        </div>
                        <div class="content">
                            <p>Hello {recipient_email.split('@')[0]},</p>
                            {personalized_message_body}
                            <div class="button-container">
                                <a href="{full_confirmation_link}" class="button">Confirm Your Email</a>
                            </div>
                            <div class="link-fallback">
                                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                                <p><a href="{full_confirmation_link}">{full_confirmation_link}</a></p>
                            </div>
                            <div class="passcode-info">
                                Your confirmation code is: <strong>{passcode}</strong>
                            </div>
                        </div>
                        <div class="footer">
                            <p>This link and code are valid for {validity_str}.</p>
                            <p>If you did not request this, please ignore this email.</p>
                            <p>&copy; {time.strftime('%Y')} Your Application Name</p>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        return html_content

    def _send_email_worker(self, recipient_email: str, subject: str, html_body: str):
        """
        The actual worker function that sends the email.
        Raises EmailSendingAuthError for authentication issues,
        EmailSendingConnectionError for connection issues,
        and EmailSendingError for other SMTP or general errors.
        """
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
            # print(error_message) # Optional: for direct library debugging
            raise EmailSendingAuthError(error_message) from e
        except smtplib.SMTPConnectError as e:
            error_message = f"SMTP Connection Error: Could not connect to {self.smtp_server}:{self.smtp_port}. {e}"
            # print(error_message)
            raise EmailSendingConnectionError(error_message) from e
        except smtplib.SMTPServerDisconnected as e:
            error_message = f"SMTP Server Disconnected: {e}. This might be a temporary issue."
            # print(error_message)
            raise EmailSendingConnectionError(error_message) from e
        except smtplib.SMTPException as e:  # Catch other specific SMTP errors
            error_message = f"An SMTP error occurred while sending email to {recipient_email}: {e}"
            # print(error_message)
            raise EmailSendingError(error_message) from e
        except Exception as e:  # Catch any other non-SMTP exceptions during the process
            error_message = f"An unexpected error occurred in _send_email_worker for {recipient_email}: {e}"
            # print(error_message)
            raise EmailSendingError(error_message) from e

    def send(self, recipient_email: str, delay_seconds: int = 0) -> str:
        """
        Generates a passcode, prepares the confirmation email, and sends it
        after an optional delay using a daemon thread.

        Args:
            recipient_email (str): The email address to send the confirmation to.
            delay_seconds (int, optional): Number of seconds to wait before sending the email.
                                           If 0, sends immediately. Defaults to 0.

        Returns:
            str: The generated passcode that was sent (or will be sent) in the email.

        Raises:
            ValueError: If recipient_email is invalid.
            EmailSendingAuthError: If SMTP authentication fails.
            EmailSendingConnectionError: If there's an issue connecting to the SMTP server.
            EmailSendingError: For other email sending related errors.
        """
        if not recipient_email or "@" not in recipient_email:
            raise ValueError("A valid recipient_email is required.")

        passcode = self._generate_passcode()

        separator = '&' if '?' in self.confirmation_link_base else '?'
        full_confirmation_link = f"{self.confirmation_link_base}{separator}passcode={passcode}"

        validity_str = self._format_duration(self.valid_for_duration_seconds)
        format_kwargs = {
            'recipient_email': recipient_email,
            'passcode': passcode,
            'validity_duration': validity_str,
            'full_confirmation_link': full_confirmation_link
        }

        final_subject = self.subject_template.format(**format_kwargs)
        html_body = self._create_html_email_body(recipient_email, passcode, full_confirmation_link)

        if delay_seconds > 0:
            email_thread = threading.Thread(
                target=self._delayed_send,
                args=(delay_seconds, recipient_email, final_subject, html_body),
                daemon=True
            )
            email_thread.start()
        else:
            self._send_email_worker(recipient_email, final_subject, html_body)  # This can raise exceptions

        return passcode

    def _delayed_send(self, delay_seconds: int, recipient_email: str, subject: str, html_body: str):
        """Helper function to handle the delay before calling _send_email_worker."""
        try:
            time.sleep(delay_seconds)
            self._send_email_worker(recipient_email, subject, html_body)
        except EmailSendingError as e:
            # Decide how to handle errors in a daemon thread.
            # For now, just printing, as raising them here won't be caught by the main thread easily.
            # A more robust solution might involve a callback or a queue for error reporting.
            print(f"Error sending email in delayed thread to {recipient_email}: {e}")
        except Exception as e:
            print(f"Unexpected error in delayed send thread for {recipient_email}: {e}")

