import mysql.connector
import sqlite3

# conn = sqlite3.connect('banking_db.db')

conn = mysql.connector.connect( 
    host="localhost",
    user="root",           # your MySQL username
    password="poopyhead2451$@d#mpy",  # the password you set during MySQL install
    database="banking_db"
)

cursor = conn.cursor()

root = tk.Tk()
root.title("University Banking Center")
root.geometry("400x420")

#add more columns or change them later

# cursor.execute("INSERT INTO account_info VALUES (1, 'Saanvi', 1000000.00)" )
# conn.commit()

# cursor.execute("SELECT * FROM account_info")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


def create_account():
    name = input("Enter your full name: ")
    college_name = input("Enter your college name: ")
    balance = 0
    tuition = float(input("Enter your tuition per semester: "))
    tuition *= int(input("Enter number of semesters attended or attending: "))
    pin_num = int(input("Create a 4 digit pin number: "))
    while True:
        if pin_num == int(input("Confirm pin: ")):
            break
        print("pins do not match")
    cursor.execute("INSERT INTO university_banking (student_name, college_name, account_balance, tuition_per_semester, pin) VALUES (%s, %s, %s, %s, %s)", (name, college_name, balance, tuition, pin_num))
    conn.commit()

def login():
    entered_name = input("Enter your full name: ")
    entered_pin = int(input("Enter your 4-digit pin: "))
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM university_banking WHERE student_name = %s AND pin = %s)",
        (entered_name, entered_pin)
    )    
    result = cursor.fetchone()[0]
    if result == 1:
        print(f"Welcome, {entered_name}")
        cursor.execute(
            "SELECT * FROM university_banking WHERE student_name = %s",
            (entered_name,)
        )
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return True
    else:
        print("Login invalid. Please try again later.")
        return False
    

has_account = input("Press 'C' to create an account or 'A' to access an existing one: ")

if has_account.lower() == "c":
    create_account()
    print("Thank you for creating an account at the Univeristy Banking Center")
elif has_account.lower() == "a":
    if not login():
        print("refresh and try again")
else:
    print("Your input is invalid")


conn.close()