import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
class CDisplayError:
    @staticmethod
    def ErrorMessage(error):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", error)
        root.destroy()

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
            if len(password) > 8 and len(username) > 4:
                hashedPw = self.HashInput(password)
                query = "INSERT INTO tblUser (Username, Password) VALUES (?, ?)"
                self.cursor.execute(query, (username, hashedPw))
                self.conn.commit()
                print(f"Inserted user '{username}' with hashed password: {hashedPw}")
                IsLoggedIn = True
                return IsLoggedIn 
            else:
                CDisplayError.ErrorMessage("Password must be Minimum 8 Characters, Username but be Minimum 4 Characters")
                IsLoggedIn = False
                return IsLoggedIn
        except sqlite3.Error as e:
            CDisplayError.ErrorMessage(f"Unable to insert {e}")
            
    def Search(self, username):
        query = "SELECT Password FROM tblUser WHERE Username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        self.conn.commit()
        #returns a tuple (result) containing the hashed password
        return result

    def Login(self,username, password):   
        result = self.Search(username)
        if result:
            storedHash = result[0] #retreiving the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), storedHash.encode('utf-8')):
                print("Logged In!")             
                return True
            else:
                CDisplayError.ErrorMessage("Incorrect Password")
                return False
        else: 
            CDisplayError.ErrorMessage("Unable To Find Username")
            return False

    def HashInput(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
            

