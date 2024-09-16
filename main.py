import pandas as pd
import sqlite3
import random

#Issues to fix:
# - ensure that no 2 IDs can be the same

con = sqlite3.connect("employees.db")
cur = con.cursor()

cur.execute("CREATE TABLE if NOT EXISTS Employees(EmployeeID, Name, Branch, Age, Salary)") 

def add_employees():
    cur.execute("SELECT * from Employees") #counts all rows in Employees table 
    emp_name = str(input("Please enter Employee's name: "))
    emp_branch = str(input("Please enter Employee's branch: "))
    emp_age = int(input("Please enter Employee's age: "))
    emp_salary = float(input("Please enter Employee's salary: "))
    
    number = random.randint(0,9999)
    letter = emp_branch[0]
    emp_id = f'{letter}{number}'
        
    data = [(emp_id, emp_name, emp_branch, emp_age, emp_salary)] #the information the user provides is be given as a tuple
    cur.executemany("INSERT INTO Employees VALUES(?, ?, ?, ?, ?)", data)
    con.commit()
    

def remove_employees():
    emp_id = [(int(input("Please enter the ID of the employee you would like to remove: ")))] #checks if employee exists
    if check_employee(emp_id):
        cur.execute("DELETE from Employees WHERE EmployeeID=?", emp_id) #SQL statement to delete selected employee
        con.commit()
        print("Employee has been successfully removed!")
    else:
        print("This employee does not exist!")
    
def update_employees(search_id):
    try:
        choice = int(input("Select an option: 1. Update EmployeeID, 2. Update Employee Name, 3. Update Employee Branch, 4. Update Employee Age, 5. Update Employee Salary, 6. Return to main menu"))
    except ValueError:
        print("Invalid input")
    
    #User is given a prompt to enter new information and then an SQL statement is executed updating the selected employee
    if choice == 1: 
        new_id = int(input("Enter new ID for employee: ")) 
        data = (new_id, search_id)
        cur.execute("UPDATE Employees SET EmployeeID = ? WHERE EmployeeID = ?", data)
        con.commit()
    elif choice == 2:
        new_name = input("Enter new name for employee: ")
        data = (new_name, search_id)
        cur.execute("UPDATE Employees SET Name = ? WHERE EmployeeID = ?" ,data)
        con.commit
    elif choice == 3:
        new_branch = input("Enter new branch for employee: ")
        data = (new_branch, search_id)
        cur.execute("UPDATE Employees SET Branch = ? WHERE EmployeeID = ?", data)
        con.commit()
    elif choice == 4:
        new_age = int(input("Enter new name for employee: "))
        data = (new_age, search_id)
        cur.execute("UPDATE Employees SET Age = ? WHERE EmployeeID = ?", data)
        con.commit()
    elif choice == 5:
        new_salary = float(input("Enter new salary for employee: "))
        data = (new_salary, search_id)        
        cur.execute("UPDATE Employees SET Salary = ? WHERE EmployeeID = ?", data)
    else: 
        pass
    
def display_employees():
    while True:     
        try: 
            choice = int(input("Select an option: 1. Display Single Employee, 2. Display all employees, 3. Display Employees by Salary, 4. Display Employees by Branch, 5. Exit "))
        except ValueError:
            print("Invalid input")
            continue
        
        if choice == 1:
            search_id = int(input("Enter the ID of the employee you want to display: ")) #Checks if employee exists
            if check_employee(search_id):
                df = pd.read_sql_query("SELECT * from Employees", con) #Selects all employees, puts into dataframe
                employee = df[df.EmployeeID == search_id] #select the employee equal to the ID entered
                print(employee) #prints employee in dataframe form
            else:
                print("This employee does not exist!")
        elif choice == 2:
            df = pd.read_sql_query("SELECT * from Employees", con)
            print(df)
        elif choice == 3:
            df = pd.read_sql_query("SELECT * from Employees ORDER BY Salary DESC", con)
            print(df)
        elif choice == 4:
            df = pd.read_sql_query("SELECT * from Employees ORDER BY Branch", con)
            print(df)
        else:
            print("Returning to main menu...\n\n")
            break
    
def check_employee(search_id):
    data = [search_id]
    cur.execute("SELECT 1 from Employees WHERE EmployeeID = ?", data)
    results = cur.fetchall()
    if len(results) == 0:
        return False
    else:
        return True
    
while True:
    print("\nWelcome to business management system!")
    try:
        choice = int(input("\n\nSelect an option: 1. Add employee, 2. Remove employee, 3. Update employee, 4. Display employee, 5. Exit "))
    except ValueError:
        print("Invalid input")
            
    if choice == 1:
        add_employees()
    elif choice == 2:
        remove_employees()
    elif choice == 3:
        search_id = int(input("Enter the ID of the employee you want to update: "))
        if check_employee(search_id):
            update_employees(search_id)
        else:
            print("This employee does not exist!")
    elif choice == 4:
        display_employees()
    elif choice == 5:
        print("Thank you, goodbye!")
        break
    else:
        print("Invalid input. Please select an option between 1 and 5")
