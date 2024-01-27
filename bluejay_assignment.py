import pandas as pd

def format_employees(data):
    #format the data and store it in employees dictionary, easy to get inference
    employees = {}
    
    for _, row in data.iterrows():
        position_id = row[0]
        position_status = row[1]
        time_in = row[2]
        time_out = row[3]
        timecard_hours = row[4]
        employee_name = row[7]

        #if the field is empty skip that particular entry
        if ':' not in str(timecard_hours):
            continue
        
        # Convert timecard hours to minutes for easy comparison
        timecard_minutes = int(timecard_hours.split(":")[0]) * 60 + int(timecard_hours.split(":")[1])
        
        if position_status == "Active":
            if position_id not in employees:
                employees[position_id] = {"name": employee_name, "positions": [{"timecard_minutes": timecard_minutes}]}
            else:
                last_position = employees[position_id]["positions"][-1]
                
                # Check if there is a gap of at least 24 hours
                if time_in != last_position:
                    employees[position_id]["positions"].append({"timecard_minutes": timecard_minutes})
                else:
                    last_position["timecard_minutes"] += timecard_minutes
    
    return employees


def worked_7consecutive_days(employees):
    emp_works_7 = []
    for position_id, employee_data in employees.items():
        for position in employee_data["positions"]:
            if len(employee_data["positions"]) >= 7:
                if [employee_data['name'],position_id] not in emp_works_7:
                    emp_works_7.append([employee_data['name'],position_id])
    return emp_works_7

def gap_gt1_lt10(employees):
    gap_1_10 = []
    for position_id, employee_data in employees.items():
        for i in range(len(employee_data["positions"]) - 1):
            current_position = employee_data["positions"][i]
            next_position = employee_data["positions"][i + 1]
            # Check if there is less than 10 hours between shifts but greater than 1 hour
            if 1 < next_position["timecard_minutes"] < 600:  # 10 hours in minutes
                if [employee_data['name'],position_id] not in gap_1_10:
                    gap_1_10.append([employee_data['name'],position_id])
    return gap_1_10

def gt14_singleShift(employees):
    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    for position_id, employee_data in employees.items():
        for position in employee_data["positions"]:
            if position["timecard_minutes"] > 840:  # 14 hours in minutes
                print(f"Name: {employee_data['name']}, Position ID: {position_id}")




excel_path = 'Assignment_Timecard.xlsx'

df = pd.read_excel(excel_path)

employees_data = format_employees(df)

#To print employees who have worked for 7 consecutive days
print("Employees who have worked for 7 consecutive days:")
work_7consec = worked_7consecutive_days(employees_data)
for entry in work_7consec:
    print(f"Name: {entry[0]}, Position ID: {entry[1]}")

#To print employees who have less than 10 hours between shifts but greater than 1 hour
print("\nEmployees who have less than 10 hours between shifts but greater than 1 hour:")
gap_1_10 = gap_gt1_lt10(employees_data)
for entry in gap_1_10:
    print(f"Name: {entry[0]}, Position ID: {entry[1]}")

#To print employees who have worked for more than 14 hours in a single shift
gt14_singleShift(employees_data)
