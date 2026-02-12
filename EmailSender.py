import smtplib
import smtplib
import ssl
from email.message import EmailMessage



# --- Email Configuration ---
sender_email = "your_email@gmail.com"
receiver_email = "recipient_email@example.com"
# Use an App Password, NOT your primary password
app_password = "your_generated_app_password" 

subject = "An Email from Python"
body = "This is a plain text email sent using Python's smtplib library."

# Create the email message object
msg = EmailMessage()
msg.set_content(body)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

# --- Send the email ---
# For Gmail, use 'smtp.gmail.com' and port 465 for SSL or 587 for starttls
smtp_server = "smtp.gmail.com"
smtp_port = 465  # Use 465 for SSL, 587 for starttls

# Create a secure SSL context
context = ssl.create_default_context()
def sendEmail(sender, recepient, **info):
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f"Summer Internship Opportunities at {info['display_name']}"
    msg['From'] = sender
    msg['To'] = recepient
try:
    # Connect to the server and send the email
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
    print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")

