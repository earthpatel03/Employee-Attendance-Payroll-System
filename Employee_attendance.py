import mysql.connector
from datetime import date

# 🔗 DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",   
    database="employee_db"
)
cursor = conn.cursor()

# ================= FUNCTIONS ================= #

# 1. Add Employee
def add_employee():
    try:
        name = input("Enter Name: ").strip()
        dept = input("Enter Department: ").strip()
        salary = int(input("Salary per day: "))

        cursor.execute(
            "INSERT INTO employees (name, department, salary_per_day) VALUES (%s,%s,%s)",
            (name, dept, salary)
        )
        conn.commit()
        print("✅ Employee Added")
    except Exception as e:
        print("❌ Error:", e)


# 2. View Employees
def view_employees():
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()

    print("\n📋 EMPLOYEES")
    for row in data:
        print(row)


# 3. Mark Attendance
def mark_attendance():
    try:
        emp_id = int(input("Enter Employee ID: "))
        status = input("Present / Absent: ").strip().capitalize()

        if status not in ["Present", "Absent"]:
            print("❌ Invalid status")
            return

        cursor.execute(
            "INSERT INTO attendance (emp_id, date, status) VALUES (%s,%s,%s)",
            (emp_id, date.today(), status)
        )
        conn.commit()

        print("✅ Attendance Marked")
    except Exception as e:
        print("❌ Error:", e)


# 4. View Attendance
def view_attendance():
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()

    print("\n📅 ATTENDANCE")
    for row in data:
        print(row)


# 5. Calculate Salary
def calculate_salary():
    try:
        emp_id = int(input("Enter Employee ID: "))

        # Count present days
        cursor.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE emp_id=%s AND status='Present'
        """, (emp_id,))
        present_days = cursor.fetchone()[0]

        # Get salary per day
        cursor.execute("SELECT salary_per_day FROM employees WHERE emp_id=%s", (emp_id,))
        result = cursor.fetchone()

        if result is None:
            print("❌ Employee not found")
            return

        per_day = result[0]
        total_salary = present_days * per_day

        print("\n💰 SALARY DETAILS")
        print("Present Days:", present_days)
        print("Salary per day:", per_day)
        print("Total Salary:", total_salary)

    except Exception as e:
        print("❌ Error:", e)


# 6. Department-wise Report
def dept_report():
    cursor.execute("""
        SELECT department, COUNT(*)
        FROM employees
        GROUP BY department
    """)

    print("\n🏢 DEPARTMENT REPORT")
    for row in cursor.fetchall():
        print("Department:", row[0], "| Employees:", row[1])


# 7. Delete Employee
def delete_employee():
    try:
        emp_id = int(input("Enter Employee ID to delete: "))

        # Step 1: delete attendance
        cursor.execute("DELETE FROM attendance WHERE emp_id=%s", (emp_id,))

        # Step 2: delete employee
        cursor.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))

        conn.commit()

        print("🗑️ Employee + Attendance Deleted")

    except Exception as e:
        print("❌ Error:", e)


# ================= MENU ================= #

while True:
    print("\n====== EMPLOYEE PAYROLL SYSTEM ======")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Mark Attendance")
    print("4. View Attendance")
    print("5. Calculate Salary")
    print("6. Department Report")
    print("7. Delete Employee")
    print("8. Exit")

    choice = input("Enter choice: ").strip()

    if choice == '1':
        add_employee()
    elif choice == '2':
        view_employees()
    elif choice == '3':
        mark_attendance()
    elif choice == '4':
        view_attendance()
    elif choice == '5':
        calculate_salary()
    elif choice == '6':
        dept_report()
    elif choice == '7':
        delete_employee()
    elif choice == '8':
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice")