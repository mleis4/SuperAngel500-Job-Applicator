# 🚀 SuperAngel500 Job Applicator
An automated CLI-based job application assistant built to streamline outreach to companies on the Superangel500 list — specifically targeting Electrical Engineering (EE) and AI/Software Engineering (AISE) roles.

This tool acts as a bridge between your curated lead lists and your inbox, helping you manage your application funnel while automating personalized outreach.

## 🛠️ Features
### 🔁 Smart Queueing
Automatically prioritizes companies that match both EE and AISE criteria, then cascades into specialized lists.
### 📧 One-Click Outreach
Prompts for a contact email and dispatches a personalized outreach email with your 2026 resume attached — all in one step.
### 📊 Live Application Tracker
Maintains a persistent application_status.csv file to track:
- Application status *(Applied, Interview, Rejected, Accepted)*
- Lead quality
- Funnel progression


## 📈 Data-Driven Insights
Displays relevant company metrics during the application process, including:
- Employee growth
- Turnover change
- Unicorn status
Helping you tailor messaging before sending outreach.

## 📁 Project Structure
```
.
├── main.py                  # Interactive command-line interface
├── EmailSender.py           # SMTP logic for sending emails
├── ApplicationStats_*.txt   # Lead data files (Both, EE, AISE)
├── application_status.csv   # Auto-generated application history
└── personalinfo.txt         # Local email credentials (NOT tracked)
```

## ⚙️ Configuration
The script requires a local file named personalinfo.txt for email authentication.
**⚠️ Do NOT upload this file to GitHub.** 
Add it to your .gitignore.
Create personalinfo.txt in the root directory with:
your_email@example.com
your_app_password



- Line 1: Your email address


- Line 2: Your App Password



## ▶️ Running the Application
python main.py

**Workflow:**


1. Select '1' to retrieve the next high-priority lead.


2. Input the company’s contact email.


3. The script:
    - Logs the application
    - Sends your resume automatically

4. Select '3' at any time to:
    - View conversion statistics
    - Check remaining lead count





## 📊 Status Tracking
The system manages your funnel through four stages:
StatusDescriptionAppliedInitial outreach completedInterviewCallback receivedRejectedApplication closedAcceptedOffer received

## 🎯 Purpose
Designed to automate the hustle — so you can focus on preparation, networking, and interviews instead of repetitive admin work.
Good luck with the applications. 🚀