import sqlite3
import bcrypt

class CCUser:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.CreateTable()

        self.cursor.execute("SELECT * FROM tblUser")
        print(self.cursor.fetchall())

    def CreateTable(self):
        #Create the user table.
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tblUser (Username VARCHAR UNIQUE, Password TEXT)"
        )
        self.conn.commit()
        print("CreatedTable")

    def Insert(self, username, password):
        #Insert a user with a hashed password.
        IsLoggedIn = False
        try:
            if len(password) > 8:
                hashedpw = self.HashInput(password)
                query = "INSERT INTO tblUser (Username, Password) VALUES (?, ?)"
                self.cursor.execute(query, (username, hashedpw))
                self.conn.commit()
                print(f"Inserted user '{username}' with hashed password: {hashedpw}")
                IsLoggedIn = True
                return IsLoggedIn 
        except sqlite3.Error as e:
            print(f"Unable to insert: {e}")
            

    def Search(self, username):
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
                return True
            return False

    def HashInput(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

