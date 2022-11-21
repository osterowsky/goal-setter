import sqlite3

# Setting _Database
try:
    db = sqlite3.connect("goals.db", check_same_thread=False)
    cur = db.cursor()
    # Creating tables if it not already exists in the database
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               username TEXT NOT NULL,
               hash TEXT NOT NULL);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
               (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               task TEXT NOT NULL,
               type TEXT NOT NULL,
               userID INTEGER,
               FOREIGN KEY (userID) REFERENCES users(ID));''')
               # For a type it could be: Plain or Finished
    cur.close()
except Exception as e:
    print("Error during connection: ", e)