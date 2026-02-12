import csv
import os

# File to store application statuses
STATUS_FILE = 'application_status.csv'

# Job list files
BOTH_JOBS_FILE = 'ApplicationStats_Both.txt'
EE_JOBS_FILE = 'ApplicationStats_EE.txt'
AISE_JOBS_FILE = 'ApplicationStats_AISE.txt'



def initialize_status_file():
    """Create the status file if it doesn't exist"""
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Status', 'Email', 'Industries', 'Turnover_Change'])
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
                    'Industries': row['Industries'],
                    'Turnover_Change': row['Turnover_Change']
                }
    except FileNotFoundError:
        pass
    return applications

def save_applications(applications):
    """Save all applications to CSV"""
    with open(STATUS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Company', 'Status', 'Email', 'Industries', 'Turnover_Change'])
        for company, data in applications.items():
            writer.writerow([
                company, 
                data['Status'], 
                data['Email'], 
                data['Industries'],
                data['Turnover_Change']
            ])

def load_job_list(filename):
    """Load jobs from a txt file"""
    jobs = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) >= 9:
                    jobs.append({
                        'id': parts[0],
                        'company': parts[1],
                        'is_unicorn': parts[2],
                        'industries': parts[3],
                        'display_name': parts[4],
                        'turnover': parts[5],
                        'employees': parts[6],
                        'employees_change': parts[7],
                        'turnover_change_percentage': parts[8],
                        'applied': parts[9]
                    })
    except FileNotFoundError:
        print(f"⚠️  {filename} not found!")
    return jobs

def get_next_unapplied_job(applications):
    """Get the next company that hasn't been applied to yet"""
    # Priority: Both > EE > AISE
    job_files = [
        (BOTH_JOBS_FILE, "Both EE & AISE"),
        (EE_JOBS_FILE, "EE"),
        (AISE_JOBS_FILE, "AISE")
    ]
    
    for filename, category in job_files:
        jobs = load_job_list(filename)
        for job in jobs:
            company = job['display_name']
            if company not in applications:
                return job, category
    
    return None, None

def add_application(applications):
    """Add next unapplied job to tracker"""
    print("\n" + "="*60)
    print("                    NEXT APPLICATION")
    print("="*60)
    
    job, category = get_next_unapplied_job(applications)
    
    if job is None:
        print("\n🎉 You've applied to all companies! Great work!")
        return
    
    print(f"\nCategory: {category}")
    print(f"Company: {job['display_name']}")
    print(f"Industries: {job['industries']}")
    print(f"Employees: {job['employees']}")
    print(f"Turnover Change: {job['turnover_change_percentage']}%")
    print(f"Is Unicorn: {job['is_unicorn']}")
    
    print("\n📧 Find their email address and enter it below:")
    email = input("Email: ").strip()
    
    if not email:
        print("❌ No email entered. Application not saved.")
        return
    
    # Save to tracker
    applications[job['display_name']] = {
        'Status': 'Applied',
        'Email': email,
        'Industries': job['industries'],
        'Turnover_Change': job['turnover_change_percentage']
    }
    
    save_applications(applications)
    print(f"\n✅ Added {job['display_name']} to tracker!")
    print("📨 TODO: Generate and send email using your email function")

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
    
    # Show remaining jobs
    total_jobs = (len(load_job_list(BOTH_JOBS_FILE)) + 
                  len(load_job_list(EE_JOBS_FILE)) + 
                  len(load_job_list(AISE_JOBS_FILE)))
    remaining = total_jobs - len(applications)
    print(f"\n📊 Remaining jobs: {remaining}/{total_jobs}")

def main():
    initialize_status_file()
    
    while True:
        print("\n" + "="*50)
        print("          JOB APPLICATION TRACKER")
        print("="*50)
        print("\n1. Apply to next company")
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