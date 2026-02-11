import csv
import ast
company_keys = ['id', 'company', 'registry_code', 'favicon', 'is_unicorn', 'industries', 'business_types', 'lists', 'display_name', 'turnover', 'labour_taxes', 'employees', 'lq_turnover', 'lq_labour_taxes', 'lq_employees', 'ly_turnover', 'ly_labour_taxes', 'ly_employees', 'employees_change', 'turnover_change_percentage', 'labour_taxes_change_percentage', 'ly_employees_change', 'ly_turnover_change_percentage', 'ly_labour_taxes_change_percentage']
csv_file = 'superangel500.csv'
company_info = []
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        temp_dict = {}
        for info in range(0, len(row)):
            data = row[info]
            if data.startswith('['):  # <-- this is the fix
                data = ast.literal_eval(data)  # properly parses the list
            temp_dict[company_keys[info]] = data
        company_info.append(temp_dict)
                
                
industries = set()
for company in company_info:
    for industry in company['industries']:
        if industry != '':
            industries.add(industry)
        

print(f"Industries: {industries}")
print('''
***********************************************************
''')

core_ee = [
    'Hardware & Electronic Equipment',
    'Machinery & Electrical',
    'Consumer Electronics & Appliances',
    'Aerospace',
    'Defence',
    'Energy',
    'Telecommunication & Services',
    'Manufacturing',
    'Automotive',
    'Medical Devices',
    'Infrastructure & Logistics',
    'Transportation',
    'Road & Rail',
    'Maritime',
    'Cleantech',
    'Engineering',
    'Research & Consulting',
    'Digital Health',
    'Agriculture, Aquaculture & Agritech',
]

# Core AISE
core_aise = [
    'Deep tech',
    'Data & Analytics',
    'Software & Services',
    'Science Tools & Services',
    'Biotechnology',
    'Research & Consulting',
    'Digital Health',
    'Medical Devices',
    'Automotive',
    'Manufacturing',
    'Agriculture, Aquaculture & Agritech',
    'Cleantech',
    'Infrastructure & Logistics',
    'Transportation',
    'Aerospace',
    'Defence',
    'Engineering'
]
def in_list(l1, l2):
    for i in l1:
        if i in l2:
            return True
    return False
keys_to_remove = [
    'registry_code',
    'favicon',
    'lists',
    'business_types',
    'lq_turnover',
    'lq_labour_taxes',
    'lq_employees',
    'ly_turnover',
    'ly_labour_taxes',
    'ly_employees',
    'labour_taxes',
    'labour_taxes_change_percentage',
    'ly_employees_change',
    'ly_turnover_change_percentage',
    'ly_labour_taxes_change_percentage',
]
for company in company_info:
    for key in keys_to_remove:
        company.pop(key, None)

aise_jobs = list(filter(lambda c: in_list(core_aise, c['industries']), company_info))
ee_jobs = list(filter(lambda c: in_list(core_ee, c['industries']), company_info))
both_jobs = list(filter(lambda c: in_list(core_aise, c['industries']) and in_list(core_ee, c['industries']), company_info))
print(f"EE jobs: {len(ee_jobs)}")
print(f"AISE jobs: {len(aise_jobs)}")
employees = [j['employees'] for j in both_jobs]
print(f"Total jobs: {(len(both_jobs))}")

# Write overlap (highest priority)
with open('ApplicationStats_Both.txt', 'w', encoding='utf-8') as f:
    keys = list(both_jobs[0].keys())
    f.write("|".join(keys) + "|Applied\n")
    for job in both_jobs:
        f.write("|".join(str(job[k]) for k in keys) + "\n")

# Write EE-only
with open('ApplicationStats_EE.txt', 'w', encoding='utf-8') as f:
    keys = list(ee_jobs[0].keys())
    f.write("|".join(keys) + "|False\n")
    for job in ee_jobs:
        f.write("|".join(str(job[k]) for k in keys) + "|False\n")

# Write AISE-only
with open('ApplicationStats_AISE.txt', 'w', encoding='utf-8') as f:
    keys = list(aise_jobs[0].keys())
    f.write("|".join(keys) + "\n")
    for job in aise_jobs:
        f.write("|".join(str(job[k]) for k in keys) + "|False\n")