import csv
import os

# File to store application statuses
STATUS_FILE = 'application_status.csv'

def initialize_status_file():
    """Create the status file if it doesn't exist"""
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Status', 'Email', 'Notes'])
        print(f"Created new status file: {STATUS_FILE}")

def load_applications():
    """Load all applications from CSV"""
    applications = {}
    try:
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                applications[row['Company']] = {
                    'Status': row['Status'],
                    'Email': row['Email'],
                    'Notes': row['Notes']
                }
    except FileNotFoundError:
        pass
    return applications

def save_applications(applications):
    """Save all applications to CSV"""
    with open(STATUS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Company', 'Status', 'Email', 'Notes'])
        for company, data in applications.items():
            writer.writerow([company, data['Status'], data['Email'], data['Notes']])

def add_application(applications):
    """Add a new job application"""
    print("\n--- Add New Application ---")
    company = input("Company name: ").strip()
    
    if company in applications:
        print(f"❌ {company} already exists in your tracker!")
        return
    
    email = input("Email (optional): ").strip()
    notes = input("Notes (optional): ").strip()
    
    applications[company] = {
        'Status': 'Applied',
        'Email': email,
        'Notes': notes
    }
    
    save_applications(applications)
    print(f"✅ Added {company} with status 'Applied'")

def update_status(applications):
    """Update the status of an existing application"""
    print("\n--- Update Application Status ---")
    
    if not applications:
        print("❌ No applications to update yet!")
        return
    
    # Show all companies
    print("\nCurrent applications:")
    for i, (company, data) in enumerate(applications.items(), 1):
        print(f"{i}. {company} - {data['Status']}")
    
    choice = input("\nEnter company name or number: ").strip()
    
    # Handle number selection
    if choice.isdigit():
        idx = int(choice) - 1
        companies = list(applications.keys())
        if 0 <= idx < len(companies):
            company = companies[idx]
        else:
            print("❌ Invalid number!")
            return
    else:
        company = choice
    
    if company not in applications:
        print(f"❌ {company} not found!")
        return
    
    print(f"\nCurrent status: {applications[company]['Status']}")
    print("\nStatus options:")
    print("1. Applied")
    print("2. Interview")
    print("3. Rejected")
    print("4. Accepted")
    
    status_choice = input("\nSelect new status (1-4): ").strip()
    status_map = {
        '1': 'Applied',
        '2': 'Interview',
        '3': 'Rejected',
        '4': 'Accepted'
    }
    
    if status_choice in status_map:
        applications[company]['Status'] = status_map[status_choice]
        save_applications(applications)
        print(f"✅ Updated {company} to '{status_map[status_choice]}'")
    else:
        print("❌ Invalid choice!")

def view_stats(applications):
    """Show application statistics"""
    print("\n--- Application Statistics ---")
    
    if not applications:
        print("No applications yet!")
        return
    
    stats = {'Applied': 0, 'Interview': 0, 'Rejected': 0, 'Accepted': 0}
    
    for company, data in applications.items():
        status = data['Status']
        if status in stats:
            stats[status] += 1
    
    print(f"\nTotal Applications: {len(applications)}")
    print(f"  Applied: {stats['Applied']}")
    print(f"  Interview: {stats['Interview']}")
    print(f"  Rejected: {stats['Rejected']}")
    print(f"  Accepted: {stats['Accepted']}")

def main():
    initialize_status_file()
    
    while True:
        print("\n" + "="*50)
        print("          JOB APPLICATION TRACKER")
        print("="*50)
        print("\n1. Add new application")
        print("2. Update application status")
        print("3. View statistics")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        applications = load_applications()
        
        if choice == '1':
            add_application(applications)
        elif choice == '2':
            update_status(applications)
        elif choice == '3':
            view_stats(applications)
        elif choice == '4':
            print("\nGood luck with your applications! 🚀")
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.")

if __name__ == "__main__":
    main()