# Passcode Link Mailer 📧✨

[![PyPI version](https://badge.fury.io/py/passcode-link-mailer.svg)](https://badge.fury.io/py/passcode-link-mailer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A straightforward Python library for sending email confirmations via Gmail using Google App Passwords.**

`passcode-link-mailer` simplifies the process of sending secure, timed email confirmations. It generates unique passcodes, embeds them in a customizable HTML email template with a confirmation link, and handles the email sending directly through your Gmail account. This library is ideal for developers seeking a direct, uncomplicated solution for email verification flows.

> **Note:** The package is named `passcode-link-mailer` but is imported as `simple_mailer`: 
> ```python
> from simple_mailer import PasscodeLinkMailer
> ```

## 🚀 Key Features

* ✅ **Gmail Focused:** Designed specifically for use with Gmail and Google App Passwords
* 🔑 **Secure Passcodes:** Leverages Python's `secrets` module to generate cryptographically strong, URL-safe passcodes
* 🎨 **Multiple Email Styles:** Choose from three professional email templates - standard, minimal, or modern
* 📂 **Template-Based Design:** Email templates are stored as HTML files for easy customization and maintenance
* ⏱️ **Customizable Validity Duration:** Allows you to specify how long the passcode should remain valid and displays this information to users
* ⏳ **Optional Delayed Sending:** Choose to send emails immediately or after a specified delay using a background thread
* 🐍 **Pure Python:** Built entirely with Python standard libraries - no external dependencies to manage
* 🛠️ **Clear Error Handling:** Provides custom exceptions to help you easily identify and handle authentication issues, connection problems, or other sending errors

## 🖼️ What the Email Looks Like

The library offers multiple email template styles. Here's an example of the standard style:

![image](https://github.com/user-attachments/assets/18a0ac21-1337-47d3-aa91-df2a9c1fb787)

Features across all template styles include:

* **Professional Header:** A clean header that establishes the purpose of the email
* **Personalized Content:** Your custom message is prominently displayed
* **Clear Call to Action:** A prominent button for confirming the email 
* **Fallback Link:** A text link in case the button doesn't work
* **Highlighted Passcode:** The confirmation code is clearly displayed in a styled box
* **Validity Information:** Users are informed how long their code remains valid
* **Responsive Design:** All templates are mobile-friendly and render well across devices

## ⚙️ Installation

Install `passcode-link-mailer` directly from PyPI:

```bash
pip install passcode-link-mailer
```

## 🔑 Prerequisites: Gmail App Password

To use this library, your Gmail account must be configured with an App Password. Standard account passwords will not work for programmatic access via smtplib and are less secure.

### Enable 2-Step Verification:
1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to the "Security" section
3. Ensure that 2-Step Verification is ON. If it's not, you'll need to set it up before you can generate an App Password

### Generate an App Password:
1. In the "Security" section of your Google Account, under "How you sign in to Google," find and click on "App passwords." (You may be required to sign in again)
2. If you don't see the "App passwords" option, it's likely that 2-Step Verification is not correctly enabled, or your Google Workspace administrator might restrict its use
3. At the bottom of the App passwords page, for "Select app," choose "Mail"
4. For "Select device," choose "Other (Custom name)"
5. Enter a descriptive name (e.g., "My Python Confirmation App" or "PasscodeLinkMailer")
6. Click "Generate"
7. Google will display a 16-character App Password (typically in a yellow bar). Copy this password (without spaces). This is the password you will use for the `gmail_app_password` parameter when initializing the mailer. Store this App Password securely, as Google will not show it to you again

## 🎨 Email Styles and Templates

The library now supports three distinct email styles, all professionally designed to help emails avoid spam filters:

1. **Standard (Default)**: A clean, professional design with a blue header and structured layout
2. **Minimal**: A simpler, lighter design for a more understated approach
3. **Modern**: A contemporary design with more visual elements and a card-based layout

To specify which style you want to use:

```python
# Using the default (standard) style
mailer = PasscodeLinkMailer(
    # ... other parameters
)

# Using the minimal style
mailer = PasscodeLinkMailer(
    # ... other parameters
    email_style='minimal'
)

# Using the modern style
mailer = PasscodeLinkMailer(
    # ... other parameters
    email_style='modern'
)
```

### Custom Template Directory

By default, templates are loaded from a `templates` directory relative to the module's location. You can specify a custom template directory if needed:

```python
mailer = PasscodeLinkMailer(
    # ... other parameters
    templates_dir='/path/to/your/custom/templates'
)
```

## ⏱️ Time Validity

The `valid_for_duration_seconds` parameter:
* Is used to generate a human-readable message for the email recipient (e.g., "This link is valid for 10 minutes")
* Does **not** actually enforce expiration timing - that's handled by your server

Your application is responsible for:
1. Recording when the passcode was created (when the `send()` method returns the passcode)
2. Implementing the expiration logic in your confirmation endpoint
3. Rejecting passcodes that have exceeded their validity period

The library is intentionally unopinionated about how you store and validate passcodes, giving you flexibility to implement whatever verification strategy makes sense for your application.

## 📝 Placeholders for Email Templates

You can use the following placeholders in your subject and message_body_template strings:

* `{recipient_email}`: The full email address of the recipient
* `{passcode}`: The generated unique passcode
* `{validity_duration}`: A user-friendly string indicating how long the link/passcode is valid (e.g., "10 minutes") - this is derived from your `valid_for_duration_seconds` value
* `{full_confirmation_link}`: The complete confirmation URL (e.g., https://mytestapp.com/confirm?passcode=UqcnqZJhCA7R51y-2wDMWBNYZSRP59Nh)

## 🛠️ How It Works

1. **Initialization:** You initialize PasscodeLinkMailer with your Gmail credentials (sender email and App Password), email content templates, the desired validity duration for the confirmation link, your application's base URL for the confirmation endpoint, and optionally specify the email style.

2. **Template Loading:** The library loads the appropriate HTML template file based on your chosen style from the templates directory.

3. **Sending a Request:** When you call the `send()` method with a recipient's email address:
   - A unique, secure passcode is generated using `secrets.token_urlsafe()`
   - The full confirmation link is constructed by appending `?passcode=THE_GENERATED_PASSCODE` to your specified base URL
   - The HTML email body is created by formatting the loaded template with your personalized message, the recipient's details, passcode, validity duration, and the confirmation link
   - The email is then sent via Gmail's SMTP server using Python's smtplib, ensuring a secure TLS connection

4. **Passcode Return:** The `send()` method returns the generated passcode. Your application should:
   - Store this passcode securely (e.g., in your database), associating it with the user and recording when it was created
   - Set up your own server-side expiration logic based on the `valid_for_duration_seconds` parameter you provided
   - When the user clicks the confirmation link in the email, your application's backend endpoint receives the passcode as a query parameter
   - Verify the received passcode against the stored one and check if it's still within its validity period to complete the confirmation process

**Important:** The library itself only generates the passcode and informs the user of the validity duration in the email. Your server is responsible for tracking when the passcode was created and enforcing the expiration time.

## 💡 Usage Example

Here's how to get started with PasscodeLinkMailer:

```python
import time  # For the example if testing delayed send

# Import the library - note the package name vs the import name
from simple_mailer import (
    PasscodeLinkMailer,
    EmailSendingAuthError,
    EmailSendingConnectionError,
    EmailSendingError
)

# --- Configuration ---
# IMPORTANT: Replace with your actual credentials for real use.
# For production, it's highly recommended to load sensitive credentials
# from environment variables or a secure configuration management system.
SENDER_GMAIL_ADDRESS = "your_test_email@gmail.com"  # Your Gmail address (the one with the App Password)
GMAIL_APP_PASSWORD = "yoursixteenletterapppassword"    # Your 16-character Gmail App Password
YOUR_APP_CONFIRM_URL_BASE = "https://mytestapp.com/confirm"  # Base URL for your app's confirmation endpoint

try:
    # Initialize the mailer with the modern style
    mailer = PasscodeLinkMailer(
        sender_email=SENDER_GMAIL_ADDRESS,
        gmail_app_password=GMAIL_APP_PASSWORD,
        subject="Test: Your Confirmation Code for MyApp",
        message_body_template=(
            "<p>Hello {recipient_email},</p>"
            "<p>This is a test email from PasscodeLinkMailer. Your code is {passcode}.</p>"
            "<p>This link is valid for {validity_duration}.</p>"
            "<p>Confirmation link: {full_confirmation_link}</p>"
        ),
        valid_for_duration_seconds=600,  # 10 minutes
        confirmation_link_base=YOUR_APP_CONFIRM_URL_BASE,
        email_style='modern'  # Try 'standard', 'minimal', or 'modern'
    )
    print("PasscodeLinkMailer initialized successfully.")

    recipient_to_confirm = "the.jar.team2025+mee@gmail.com"  # Replace with your actual recipient
    
    # --- Send an email immediately ---
    print(f"Sending immediate confirmation to {recipient_to_confirm}...")
    passcode1 = mailer.send(recipient_email=recipient_to_confirm, delay_seconds=0)
    print(f"Immediate email sent! Passcode: {passcode1}")
    print(f"Please check {recipient_to_confirm}'s inbox.")

    # --- Example: Send an email with a 5-second delay ---
    print(f"\nSending delayed confirmation to {recipient_to_confirm} (5s delay)...")
    delayed_passcode = mailer.send(recipient_email=recipient_to_confirm, delay_seconds=5)
    print(f"Delayed email request initiated. Passcode generated: {delayed_passcode}")
    print("Email will be sent by a background thread in approximately 5 seconds.")
    print("Main script will wait for 15 seconds to allow the thread to complete.")
    time.sleep(15)  # Keep main thread alive for daemon thread to work
    print(f"Check {recipient_to_confirm} for the delayed email.")

except ValueError as ve:
    print(f"Configuration or Input Error: {ve}")
except EmailSendingAuthError as auth_err:
    print(f"Authentication Failed: {auth_err}")
    print("ACTION REQUIRED: Double-check your SENDER_GMAIL_ADDRESS and GMAIL_APP_PASSWORD. "
          "Ensure 2-Step Verification and the App Password are correctly set up in your Google Account.")
except EmailSendingConnectionError as conn_err:
    print(f"Connection Error: {conn_err}")
    print("Could not connect to Gmail's SMTP server. Check your internet connection or firewall settings.")
except EmailSendingError as send_err:
    print(f"A general email sending error occurred: {send_err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## 📝 Full Example Test Script

Here's a complete test script that you can use to verify your configuration:

```python
import time
from simple_mailer import (
    PasscodeLinkMailer,
    EmailSendingAuthError,
    EmailSendingConnectionError,
    EmailSendingError
)

if __name__ == "__main__":
    print("Starting PasscodeLinkMailer Test Script...")

    # --- IMPORTANT: Configuration for Local Testing ---
    # 1. Ensure 2-Step Verification is enabled on your Gmail account.
    # 2. Generate an App Password: https://myaccount.google.com/apppasswords
    #    (Select "Mail" and "Other (Custom name)" for the app, e.g., "My Python Test Script")
    # 3. Replace the placeholders below with your actual credentials and details.

    # --- !!! REPLACE WITH YOUR ACTUAL TEST CREDENTIALS !!! ---
    SENDER_GMAIL_ADDRESS = "your_test_email@gmail.com"  # Your Gmail address for sending
    GMAIL_APP_PASSWORD = "yoursixteenletterapppassword"    # The 16-character App Password (no spaces)
    TEST_RECIPIENT_EMAIL = "recipient_test_email@example.com" # Email address to send the test to
    # --- !!! END OF CREDENTIALS SECTION !!! ---

    if SENDER_GMAIL_ADDRESS == "your_test_email@gmail.com" or \
       GMAIL_APP_PASSWORD == "yoursixteenletterapppassword" or \
       TEST_RECIPIENT_EMAIL == "recipient_test_email@example.com":
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! WARNING: Please update placeholder credentials in the __main__ block. !!!")
        print("!!! This script will likely fail until you provide real test credentials. !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        # You might want to exit here if placeholders are still present
        # import sys
        # sys.exit("Exiting due to placeholder credentials.")

    print(f"Attempting to initialize PasscodeLinkMailer with sender: {SENDER_GMAIL_ADDRESS}")

    try:
        # Try each of the available styles
        for style in ['standard', 'minimal', 'modern']:
            print(f"\n--- Testing with {style.upper()} email style ---")
            
            mailer = PasscodeLinkMailer(
                sender_email=SENDER_GMAIL_ADDRESS,
                gmail_app_password=GMAIL_APP_PASSWORD,
                subject=f"Test: {style.capitalize()} Style Email from PasscodeLinkMailer",
                message_body_template="<p>Hello {recipient_email},</p>\
                <p>This is a test email using the <strong>{style}</strong> template style.</p>\
                <p>Your code is {passcode}.</p>\
                <p>This link is valid for {validity_duration}.</p>",
                valid_for_duration_seconds=600,  # 10 minutes for testing
                confirmation_link_base="https://mytestapp.com/confirm",
                email_style=style
            )
            print(f"{style.capitalize()} style mailer initialized successfully.")

            # Send test email with this style
            try:
                passcode = mailer.send(recipient_email=TEST_RECIPIENT_EMAIL, delay_seconds=0)
                print(f"{style.capitalize()} email sent. Passcode: {passcode}")
                print(f"Check {TEST_RECIPIENT_EMAIL} for the email.")
                
                # Wait between emails to avoid Gmail rate limiting
                if style != 'modern':  # Don't wait after the last one
                    print("Waiting 10 seconds before next test...")
                    time.sleep(10)
                    
            except Exception as e_send:
                print(f"Error sending {style} email: {e_send}")

        print("\n--- Test Script Finished ---")
        print(f"Check {TEST_RECIPIENT_EMAIL} for all three email styles!")

    except ValueError as ve_init:
        print(f"Initialization Error: {ve_init}")
        print("This usually means sender_email or gmail_app_password in __init__ was invalid.")
    except Exception as e_init:
        print(f"An unexpected error occurred during mailer initialization: {e_init}")
```

## 🙌 Contributing

Contributions, bug reports, and feature requests are warmly welcome! We encourage you to help improve passcode-link-mailer.

* Found a bug or have an idea? Please open an issue on the GitHub Issues page

## 📜 License

This project is licensed under the MIT License. You can find the full license text in the LICENSE file in the repository.

---

*This library is intended for simple, direct email confirmation needs. For more complex requirements or enterprise-grade email solutions, consider using dedicated email service providers.*
