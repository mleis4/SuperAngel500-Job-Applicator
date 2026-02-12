import smtplib
import smtplib
import ssl
from email.message import EmailMessage

info = {
    'display_name': 'Veriff',
    'industries': ['Fintech', 'Software & Services'],
    'is_unicorn': 'False',
    'employees': '324',
    'turnover': '24191850.79',
    'turnover_change_percentage': '40',
}

# Create a secure SSL context

def sendEmail(recipient, info, *pdf_paths):
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    with open('personalinfo.txt', 'r') as f:
        lines = f.readlines()
        sender = lines[0].strip()
        password = lines[1].strip()
    
    body = ""
    with open('Email.txt', mode='r', newline='', encoding='utf-8') as file:
        for line in file:
            body += line
    
    body = body.replace("[Company Name]", info['display_name'].lower().capitalize())
    
    if len(info['industries']) > 1:
        temp = "the " + ", ".join(info['industries'][:-1]) + f" and {info['industries'][-1]}"
    else:
        temp = "the " + info['industries'][0]
    
    body = body.replace("[Industry]", temp)
    
    if float(info['turnover_change_percentage']) > 20:
        body = body.replace("[Turnover Change %]", 
            f" I was also impressed to see your {info['turnover_change_percentage']}% quarter-over-quarter growth, which speaks to the momentum and opportunity within the company.")
    else:
        body = body.replace("[Turnover Change %]", " ")
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f"Summer Internship Opportunities at {info['display_name'].lower().capitalize()}"
    msg['From'] = sender
    msg['To'] = recipient
    
    # Attach all PDFs
    for pdf_path in pdf_paths:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            filename = pdf_path.split('/')[-1].split('\\')[-1]  # handles both / and \
            msg.add_attachment(pdf_data, maintype='application', subtype='pdf', 
                             filename=filename)
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

