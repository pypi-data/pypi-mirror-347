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

        # Format the passcode with spaces for better readability
        formatted_passcode = " ".join(passcode[i:i + 3] for i in range(0, len(passcode), 3))

        personalized_message_body = self.message_body_template.format(
            recipient_email=recipient_email,
            passcode=formatted_passcode,
            validity_duration=validity_str,
            full_confirmation_link=full_confirmation_link
        )

        # Year for copyright footer
        current_year = time.strftime('%Y')

        # Improved HTML styling for better deliverability and appearance
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="color-scheme" content="light">
                <meta name="supported-color-schemes" content="light">
                <title>Email Confirmation</title>
                <!--[if mso]>
                <noscript>
                    <xml>
                        <o:OfficeDocumentSettings>
                            <o:PixelsPerInch>96</o:PixelsPerInch>
                        </o:OfficeDocumentSettings>
                    </xml>
                </noscript>
                <![endif]-->
                <style>
                    /* Base styles */
                    body, html {{
                        margin: 0 auto !important;
                        padding: 0 !important;
                        height: 100% !important;
                        width: 100% !important;
                        font-family: Arial, Helvetica, sans-serif !important;
                        font-size: 16px;
                        line-height: 1.5;
                        color: #444444;
                    }}
                    * {{
                        -ms-text-size-adjust: 100%;
                        -webkit-text-size-adjust: 100%;
                    }}
                    table, td {{
                        mso-table-lspace: 0pt !important;
                        mso-table-rspace: 0pt !important;
                    }}
                    table {{
                        border-spacing: 0 !important;
                        border-collapse: collapse !important;
                        table-layout: fixed !important;
                        margin: 0 auto !important;
                    }}
                    img {{
                        -ms-interpolation-mode: bicubic;
                        border: 0;
                    }}
                    a {{
                        color: #0366d6;
                        text-decoration: none;
                    }}
                    .button-td, .button-a {{
                        transition: all 100ms ease-in;
                    }}
                    .button-td:hover, .button-a:hover {{
                        background-color: #0056b3 !important;
                        border-color: #0056b3 !important;
                    }}
                    /* Media Queries */
                    @media screen and (max-width: 600px) {{
                        .email-container {{
                            width: 100% !important;
                            max-width: 100% !important;
                        }}
                        .fluid {{
                            max-width: 100% !important;
                            height: auto !important;
                            margin-left: auto !important;
                            margin-right: auto !important;
                        }}
                    }}
                </style>
            </head>
            <body width="100%" style="margin: 0; padding: 0 !important; background-color: #f5f7fa;">
                <center role="article" aria-roledescription="email" lang="en" style="width: 100%; background-color: #f5f7fa;">
                    <!--[if mso | IE]>
                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f5f7fa;">
                    <tr>
                    <td>
                    <![endif]-->

                    <!-- Email Body -->
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="margin: auto; background-color: #ffffff;" class="email-container">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 25px 0; text-align: center; background-color: #0366d6;">
                                <h1 style="margin: 0; font-size: 24px; font-weight: normal; color: #ffffff;">Verify Your Email</h1>
                            </td>
                        </tr>

                        <!-- Content -->
                        <tr>
                            <td style="padding: 30px; text-align: left;">
                                {personalized_message_body}
                            </td>
                        </tr>

                        <!-- Button -->
                        <tr>
                            <td style="padding: 0 30px 30px; text-align: center;">
                                <!-- Button : BEGIN -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td style="border-radius: 4px; background-color: #0366d6; text-align: center;" class="button-td">
                                            <a href="{full_confirmation_link}" style="background-color: #0366d6; border: 15px solid #0366d6; font-family: sans-serif; font-size: 16px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 4px; font-weight: 500; color: #ffffff !important;" class="button-a">
                                                Confirm Email
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                <!-- Button : END -->
                            </td>
                        </tr>

                        <!-- Fallback Link -->
                        <tr>
                            <td style="padding: 0 30px 20px; text-align: center; color: #666666; font-size: 14px;">
                                If the button doesn't work, copy and paste this link:
                                <br>
                                <a href="{full_confirmation_link}" style="color: #0366d6; word-break: break-all;">{full_confirmation_link}</a>
                            </td>
                        </tr>

                        <!-- Passcode Box -->
                        <tr>
                            <td style="padding: 0 30px 30px;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f9fa; border-left: 4px solid #0366d6; border-radius: 4px;">
                                    <tr>
                                        <td style="padding: 20px; text-align: left; font-size: 15px; color: #444444;">
                                            <p style="margin: 0 0 10px 0;">Your confirmation code:</p>
                                            <p style="margin: 0; font-size: 20px; font-weight: bold; letter-spacing: 1px; color: #0366d6; font-family: monospace;">{formatted_passcode}</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px 30px; background-color: #f5f5f5; text-align: center; color: #777777; font-size: 13px; border-top: 1px solid #e5e5e5;">
                                <p style="margin: 0 0 5px 0;">This link and code are valid for {validity_str}.</p>
                                <p style="margin: 0 0 5px 0;">If you didn't request this email, please disregard it.</p>
                                <p style="margin: 0;">&copy; {current_year} Your Company Name</p>
                            </td>
                        </tr>
                    </table>
                    <!--[if mso | IE]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                </center>
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

