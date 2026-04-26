import tkinter as tk
from tkinter import messagebox
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="poopyhead2451$@d#mpy",
    database="banking_db"
)

cursor = conn.cursor()

#main window
root = tk.Tk()
root.title("University Banking Center")
root.geometry("400x420")

# clear existing widgets
def clear():
    for widget in root.winfo_children():
        widget.destroy()

# home screen 
def show_home():
    clear()
    tk.Label(root, text="University Banking Center", font=("Arial", 16, "bold")).pack(pady=30)
    tk.Button(root, text="Create Account", width=20, command=show_create).pack(pady=8)
    tk.Button(root, text="Login",          width=20, command=show_login).pack(pady=8)

# create an account
def show_create():
    clear()
    tk.Label(root, text="Create Account", font=("Arial", 14, "bold")).pack(pady=16)

    tk.Label(root, text="Full Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="College Name").pack()
    entry_college = tk.Entry(root)
    entry_college.pack()

    tk.Label(root, text="Tuition per Semester").pack()
    entry_tuition = tk.Entry(root)
    entry_tuition.pack()

    tk.Label(root, text="Semesters").pack()
    entry_sems = tk.Entry(root)
    entry_sems.pack()

    tk.Label(root, text="PIN (4 digits)").pack()
    entry_pin = tk.Entry(root, show="*")
    entry_pin.pack()

    tk.Label(root, text="Confirm PIN").pack()
    entry_pin2 = tk.Entry(root, show="*")
    entry_pin2.pack()

    status = tk.Label(root, text="", fg="red")
    status.pack(pady=4)

    def submit():
        name    = entry_name.get().strip()
        college = entry_college.get().strip()
        tui_str = entry_tuition.get().strip()
        sem_str = entry_sems.get().strip()
        pin_str = entry_pin.get().strip()
        pin2    = entry_pin2.get().strip()

        if not all([name, college, tui_str, sem_str, pin_str, pin2]):
            status.config(text="All fields are required.")
            return
        if len(pin_str) != 4 or not pin_str.isdigit():
            status.config(text="PIN must be exactly 4 digits.")
            return
        if pin_str != pin2:
            status.config(text="PINs do not match.")
            return
        try:
            tuition = float(tui_str) * int(sem_str)
        except ValueError:
            status.config(text="Invalid numeric input.")
            return

        cursor.execute(
            "INSERT INTO university_banking (student_name, college_name, account_balance, tuition_per_semester, pin) VALUES (%s, %s, %s, %s, %s)",
            (name, college, 0.00, tuition, int(pin_str))
        )
        conn.commit()
        messagebox.showinfo("Success", f"Account created for {name}!")
        show_home()

    tk.Button(root, text="Submit", command=submit).pack(pady=8)
    tk.Button(root, text="Back",   command=show_home).pack()

# login
def show_login():
    clear()
    tk.Label(root, text="Login", font=("Arial", 14, "bold")).pack(pady=16)

    tk.Label(root, text="Full Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="PIN").pack()
    entry_pin = tk.Entry(root, show="*")
    entry_pin.pack()

    status = tk.Label(root, text="", fg="red")
    status.pack(pady=4)

    def submit():
        name    = entry_name.get().strip()
        pin_str = entry_pin.get().strip()

        if not name or not pin_str:
            status.config(text="Please fill in all fields.")
            return
        if not pin_str.isdigit():
            status.config(text="Transaction must be numeric.")
            return

        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM university_banking WHERE student_name = %s AND pin = %s)",
            (name, int(pin_str))
        )
        found = cursor.fetchone()[0]

        if found:
            cursor.execute(
                "SELECT student_name, college_name, account_balance, tuition_per_semester FROM university_banking WHERE student_name = %s AND pin = %s",
                (name, int(pin_str))
            )
            row = cursor.fetchone()
            show_dashboard(row)
        else:
            status.config(text="Invalid name or PIN.")

    tk.Button(root, text="Login", command=submit).pack(pady=8)
    tk.Button(root, text="Back",  command=show_home).pack()

def make_deposit():
    clear()
    tk.Label(root, text="Deposit", font=("Arial", 14, "bold")).pack(pady=16)

    tk.Label(root, text="Full Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Deposite Amount").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    status = tk.Label(root, text="", fg="red")
    status.pack(pady=4)

    def submit():
        name = entry_name.get().strip()
        deposit_amount = entry_amount.get().strip()

        if not name or not deposit_amount:
            status.config(text="Please fill in all fields.")
            return
        try:
            deposit_amount = float(deposit_amount)
        except ValueError:
            status.config(text="Amount must be a valid number.")
            return

        cursor.execute(
        "UPDATE university_banking SET account_balance = account_balance + %s WHERE student_name = %s",
        (float(deposit_amount), name)
        )
        
        conn.commit()

        cursor.execute(
            "INSERT INTO transactions (student_name, amount) VALUES (%s, %s)",
            (name, deposit_amount)
        )
        conn.commit()

        status.config(text="Deposit successful")

    tk.Button(root, text="Submit Deposit", command=submit).pack(pady=8)
    tk.Button(root, text="Back",  command=show_home).pack()

def make_withdrawl():
    clear()
    tk.Label(root, text="Withdrawl", font=("Arial", 14, "bold")).pack(pady=16)

    tk.Label(root, text="Full Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Withdrawl Amount").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    status = tk.Label(root, text="", fg="red")
    status.pack(pady=4)

    def submit():
        name = entry_name.get().strip()
        withdrawl_amount = entry_amount.get().strip()

        if not name or not withdrawl_amount:
            status.config(text="Please fill in all fields.")
            return
        try:
            withdrawl_amount = float(withdrawl_amount)
        except ValueError:
            status.config(text="Amount must be a valid number.")
            return

        cursor.execute(
        "UPDATE university_banking SET account_balance = account_balance - %s WHERE student_name = %s",
        (float(withdrawl_amount), name)
        )
        conn.commit()

        cursor.execute(
            "INSERT INTO transactions (student_name, amount) VALUES (%s, %s)",
            (name, float(-withdrawl_amount))
        )
        conn.commit()
        
    tk.Button(root, text="Submit Withdrawl", command=submit).pack(pady=8)
    tk.Button(root, text="Back",  command=show_home).pack()

def tansaction_history():
    clear()
    tk.Label(root, text="See Transactions", font=("Arial", 14, "bold")).pack(pady=16)


    tk.Label(root, text="Full Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="PIN").pack()
    entry_pin = tk.Entry(root, show="*")
    entry_pin.pack()

    def submit():
        name    = entry_name.get().strip()
        pin_str = entry_pin.get().strip()

        if not name or not pin_str:
            status.config(text="Please fill in all fields.")
            return
        if not pin_str.isdigit():
            status.config(text="Transaction must be numeric.")
            return

        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM university_banking WHERE student_name = %s AND pin = %s)",
            (name, int(pin_str))
        )
        found = cursor.fetchone()[0]
        conn.commit()

        cursor.execute(
                "SELECT student_name, amount, activity_date FROM transactions WHERE student_name = %s",
                (name,)
            )
        rows = cursor.fetchall()

        for row in rows:
            tk.Label(root, text=f"{row[2]}  |  ${row[1]:,.2f}").pack()



    tk.Button(root, text="See History", command=submit).pack(pady=8)
    tk.Button(root, text="Go Home",  command=show_home).pack()



# dashboard
def show_dashboard(row):
    clear()
    name, college, balance, tuition = row
    tk.Label(root, text=f"Welcome, {name}!", font=("Arial", 14, "bold")).pack(pady=16)
    tk.Label(root, text=f"College: {college}").pack()
    tk.Label(root, text=f"Balance: ${balance:,.2f}").pack(pady=8)
    tk.Label(root, text=f"Total Tuition: ${tuition:,.2f}").pack(pady=8)
    tk.Label(root, text="********************************************************************").pack(pady=8)
    tk.Button(root, text="Deposit", command=make_deposit).pack(pady=8)
    tk.Button(root, text="Withdrawl", command=make_withdrawl).pack(pady=8)
    tk.Button(root, text="See Transaction History", command=tansaction_history).pack(pady=8)
    tk.Label(root, text="********************************************************************").pack(pady=8)
    tk.Button(root, text="Log Out", command=show_home).pack(pady=16)


show_home()
root.mainloop()

conn.close()