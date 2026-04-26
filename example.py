
import sqlite3

# Step 1: Connect to a database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Step 2: Run SQL commands
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# Step 3: Process results
for row in rows:
    print(row)

# Step 4: Close the connection
conn.close()
'poopyhead2451$@d#mpy'