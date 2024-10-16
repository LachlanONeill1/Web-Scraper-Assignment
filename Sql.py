import sqlite3
import bcrypt

class CCUser:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.CreateTable()
        self.Insert("John55", "hi")  
        self.Login("John55", "hi")

    def CreateTable(self):
        #Create the user table.
        self.cursor.execute("DROP TABLE IF EXISTS tblUser")
        self.conn.commit()
        self.cursor.execute(
            "CREATE TABLE tblUser (Username VARCHAR UNIQUE, Password TEXT)"
        )
        self.conn.commit()

    def Insert(self, username, password):
        #Insert a user with a hashed password.
        try:
            hashedpw = self.HashInput(password)
            query = "INSERT INTO tblUser (Username, Password) VALUES (?, ?)"
            self.cursor.execute(query, (username, hashedpw))
            self.conn.commit()
            print(f"Inserted user '{username}' with hashed password: {hashedpw}")
        except sqlite3.Error as e:
            print(f"Unable to insert: {e}")

    def Search(self, username):
        #Search for the user by username and return the password hash.
        query = "SELECT Password FROM tblUser WHERE Username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        self.conn.commit()
        return result

    def Login(self,username, password):
       
        result = self.Search(username)
        if result:
            stored_hash = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("Logged In!")
            else:
                print("Incorrect password.")
        else:
            print("Username not found.")

    def HashInput(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

