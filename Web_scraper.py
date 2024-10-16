from graph import Graph
from Sql import CCUser
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
import datetime
from datetime import datetime
import bcrypt
import sqlite3


#from Web_scraper2 import App2
# frame_color = root.cget("fg_color")
#fg_color=frame_color
crypto_name = ['Bitcoin', 'Ethereum', 'Tether', 'Binance Coin', 'Cardano', 'XRP', 'Solana', 'Polkadot', 'Dogecoin', 'Shiba Inu', 'Avalanche', 'Chainlink', 'Uniswap', 'Litecoin', 'Stellar', 'VeChain', 'Theta', 'TRON', 'Monero', 'EOS', 'Cosmos', 'Aave', 'IOTA', 'Tezos', 'FTX Token', 'NEO', 'Kusama', 'Dash', 'Zcash', 'Waves', 'Compound', 'Maker', 'Huobi Token', 'SushiSwap', 'Terra', 'Algorand', 'Celo', 'Enjin Coin', 'Zilliqa', 'Decred', 'Qtum', 'OMG Network', 'Hedera', 'Harmony', 'Fantom', '1inch', 'Chiliz', 'Synthetix', 'Basic Attention Token', 'Yearn.Finance', 'Artificial Superintelligence Alliance', 'BNB', 'Polygon']
crypto_symbols = ['BTC-AUD', 'ETH-AUD', 'USDT-AUD', 'BNB-AUD', 'ADA-AUD', 'XRP-AUD', 'SOL-AUD', 'DOT-AUD', 'DOGE-AUD', 'SHIB-AUD', 'AVAX-AUD', 'LINK-AUD', 'UNI-AUD', 'LTC-AUD', 'XLM-AUD', 'VET-AUD', 'THETA-AUD', 'TRX-AUD', 'XMR-AUD', 'EOS-AUD', 'ATOM-AUD', 'AAVE-AUD', 'MIOTA-AUD', 'XTZ-AUD', 'FTT-AUD', 'NEO-AUD', 'KSM-AUD', 'DASH-AUD', 'ZEC-AUD', 'WAVES-AUD', 'COMP-AUD', 'MKR-AUD', 'HT-AUD', 'SUSHI-AUD', 'LUNA-AUD', 'ALGO-AUD', 'CELO-AUD', 'ENJ-AUD', 'ZIL-AUD', 'DCR-AUD', 'QTUM-AUD', 'OMG-AUD', 'HBAR-AUD', 'ONE-AUD', 'FTM-AUD', '1INCH-AUD', 'CHZ-AUD', 'SNX-AUD', 'BAT-AUD', 'YFI-AUD', 'ASI-AUD', 'BNB-AUD', 'MATIC-AUD']
crypto_dict = dict(zip(crypto_name, crypto_symbols))

class frmLogin():
    def __init__(self):
        user = CCUser("User.db")
        user.CreateTable()
      
        

        self.root = ctk.CTk()  
        self.root.title("Login & Signup")
        self.root.geometry("400x300")

        # Create Login Frame 
        login_frame = ctk.CTkFrame(self.root)
        login_frame.grid(row=0, column=0, padx=10, pady=10)

        login_label = ctk.CTkLabel(login_frame, text="Login")
        login_label.pack(pady=5)

        self.login_entry = ctk.CTkEntry(login_frame, placeholder_text="Username")
        self.login_entry.pack(pady=5)

        login_button = ctk.CTkButton(login_frame, text="Login", command=self.launch_app)
        login_button.pack(pady=10)

        # Create Signup Frame 
        signup_frame = ctk.CTkFrame(self.root)
        signup_frame.grid(row=0, column=1, padx=10, pady=10)

        signup_label = ctk.CTkLabel(signup_frame, text="Sign Up")
        signup_label.pack(pady=5)

        self.signup_entry = ctk.CTkEntry(signup_frame, placeholder_text="New Username")
        self.signup_entry.pack(pady=5)

        signup_button = ctk.CTkButton(signup_frame, text="Sign Up")
        signup_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def launch_app(self):  
        self.root.destroy()  
        app = App()  

  

    def on_close(self):
        self.root.destroy()




        

class App:
    def __init__(self):
        self.symbols = []
        self.lista = []
        self.get_cryptos('https://www.coinspot.com.au/')
        self.main() 

    def main(self):                            
       #Sets the default gui theme and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # root window
        self.root = ctk.CTk()  #
        self.root.title("Webscraper")
        self.root.geometry('1300x800')
        self.root.resizable(False, False)
       
        usdToAud = 1.5

    
        # Widget menu frame
        widgetmenu = ctk.CTkFrame(self.root, height=550, width=350, corner_radius=8)
        widgetmenu.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        cmbThemes = ctk.CTkComboBox(widgetmenu, corner_radius=8, values=['Dark Mode', "Light Mode"], command=self.changeTheme)
        cmbThemes.grid(row=0, column=0, pady=(10, 0))
        cmbThemes.set("Dark")
        uiScale = ctk.CTkOptionMenu(widgetmenu, values=["80%", "90%", "100%", "110%", "120%"], command=self.UiScaling)
        uiScale.grid(row=1,column=0, padx=20, pady=20, sticky="n")
        btnExport = ctk.CTkButton(widgetmenu,corner_radius=8,text="export all values to txtFile", command=self.export_to_txt)
        btnExport.grid(row=2,column=0,pady=20,padx=20)

        # Main menu frame
        mainmenu = ctk.CTkFrame(self.root, height=750, width=1225, corner_radius=8)
        mainmenu.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        lblWelcome = ctk.CTkLabel(mainmenu, corner_radius=8,width=1,height=50,text="Lachlans Crypto Scraper", font=ctk.CTkFont(family='Arial', size=40))
        lblWelcome.grid(row=0,column=0,padx=20, pady=20)
        lblMessage = ctk.CTkLabel(mainmenu, corner_radius=8,width=50,height=50,text="All Graphs in AUD", font=ctk.CTkFont(family='Arial', size=10))
        lblMessage.grid(row=0,column=1,padx=20, pady=20)
        btnBitcoin = ctk.CTkLabel(mainmenu, corner_radius=8,text=f"{self.lista[0]}, Currency: {self.CleanValue(self.lista[1])}", width=300)
        btnBitcoin.grid(row=1,column=0,padx=20, pady=20, sticky="n")
        btnLitecoin = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[2]}, Currency: {self.lista[3]}", width=300)
        btnLitecoin.grid(row=2,column=0,padx=20, pady=20)
        btnEthereum = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[4]}, Currency: {self.lista[5]}", width=300)
        btnEthereum.grid(row=3,column=0,padx=20, pady=20)
        btnSolana = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[6]}, Currency: {self.lista[7]}",width=300)
        btnSolana.grid(row=4,column=0,padx=20, pady=20)
        btnSyscoin = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[8]}, Currency: {self.lista[9]}", width=300)
        btnSyscoin.grid(row=5,column=0,padx=20, pady=20)
        btnGraph1 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[0]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[0])))
        btnGraph1.grid(row=1,column=1,padx=20, pady=20, sticky="n")
        btnGraph2 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[2]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[2])))
        btnGraph2.grid(row=2,column=1,padx=20, pady=20, sticky="n")
        btnGraph3 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[4]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[4])))
        btnGraph3.grid(row=3,column=1,padx=20, pady=20, sticky="n")
        btnGraph4 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[6]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[6])))
        btnGraph4.grid(row=4,column=1,padx=20, pady=20, sticky="n")
        btnGraph5 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[8]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[8])))
        btnGraph5.grid(row=5,column=1,padx=20, pady=20, sticky="n")

        #Footer
        Footer = ctk.CTkFrame(self.root, height=300, width=1225, corner_radius=8)
        Footer.grid(row=4, column=1,padx=20, pady=20, sticky="n")
        lblConnection = ctk.CTkLabel(Footer,corner_radius=8,text=f"{self.ConnectionSate(url = 'https://www.coinspot.com.au/')}", width=880,font=ctk.CTkFont(family='Arial', size=40))
        lblConnection.grid(row=0,column=0,padx=20, pady=20, sticky="n")
        lblSelect = ctk.CTkLabel(Footer, corner_radius=8, text="If your are experiencing Issues, Please select Another Website.")
        lblSelect.grid(row=1,column=0,padx=20, pady=5, sticky="n")
        lblSelect2 = ctk.CTkLabel(Footer, corner_radius=8, text="Warning. If you switch Website, The displayed cryptos may change.")
        lblSelect2.grid(row=2,column=0,padx=20, pady=5, sticky="n")
        cbxWebsite = ctk.CTkComboBox(Footer,corner_radius=9, values= ['Coinspot', 'Crypto.com'], command= self.CheckCBX)
        cbxWebsite.set("Coinspot")
        cbxWebsite.grid(row=3,column=0,padx=20, pady=5, sticky="n")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
       


        self.root.mainloop() 
    def CheckCBX(self, cbx):
        if cbx == 'Crypto.com':
            self.root.destroy()
            App2()
        

    #Theme Change Function
    def changeTheme(self, choice):  
        if choice == "Dark Mode":
            ctk.set_appearance_mode("dark")
        elif choice == "Light Mode":
            ctk.set_appearance_mode("light")

    def CleanValue(self,list):
        clean = list.replace(",", "").replace(".", "").replace("$","")
        
        return clean

    def on_close(self):
        self.root.destroy()

    #UI Scaling Function
    def UiScaling(self, scalingValue):
        match scalingValue:
            case "80%":
                ctk.set_widget_scaling(0.8)
            case "90%":
                ctk.set_widget_scaling(0.9)
            case "100%":
                ctk.set_widget_scaling(1.0)
            case "110%":
                ctk.set_widget_scaling(1.1)
            case "120%":
                ctk.set_widget_scaling(1.2)

    # Export current top cryptos and their values to txt File
    def export_to_txt(self):
        date = datetime.today().strftime('%d-%m-%Y')
        #Using the default extension to default it to a txt file
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=f"{date} Cryptos")
        if file_path:
            #Opens file manager and asks where you would like to store the file
            with open(file_path, 'w') as file:
                for item in self.lista:
                    file.write(f"{item}\n")
            messagebox.showinfo("Export", "Data exported successfully!")
    
    def ConnectionSate(self, url):
        r = requests.head(url)
        if r.status_code == 200:
            print("Website up!")
            return "Website Up!"
              
    #This function goes and gets the top 5 cryptos from coinspot
    def get_cryptos(self, url):
        URL = url
        response = requests.get(URL)
        response.status_code
            

        soup = BeautifulSoup(response.content, 'html.parser')
        table=soup.find('table', {'class':'cstable'})
        name = soup.find('span',{'class':'coinname hidden-xs'})
        value = soup.find('td', {'class':'mont fs-16'})
        rows = table.find_all('tr')
        
        #self.lista = []

        for row in rows:
            name = row.find('span', {'class': 'coinname hidden-xs'})
            value = row.find('td', {'class': 'mont fs-16'})
            if name is not None and value is not None:
                #Appends each of them into a list so i am able to display them  
                self.lista.append(name.text.strip())
                self.lista.append(value.text.strip())
                #print(name.text.strip() + ' ' + value.text.strip())
        print(self.lista)    
        print(self.CleanValue("23.53,4"))
       



class App2():
    def __init__(self):
        self.crypto_details("https://crypto.com/price")
        self.main()
        self.symbols = []
        self.lista = []
    def main(self):
        self.root1 = ctk.CTk()  #
        self.root1.title("Webscraper")
        self.root1.geometry('1300x800')
        self.root1.resizable(False, False)
        usdToAud = 1.5
        
    # Print the resulting list of symbols
                           
       #Sets the default gui theme and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
    
        # Widget menu frame
        widgetmenu = ctk.CTkFrame(self.root1, height=550, width=350, corner_radius=8)
        widgetmenu.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        cmbThemes = ctk.CTkComboBox(widgetmenu, corner_radius=8, values=['Dark Mode', "Light Mode"], command=self.changeTheme)
        cmbThemes.grid(row=0, column=0, pady=(10, 0))
        cmbThemes.set("Dark")
        uiScale = ctk.CTkOptionMenu(widgetmenu, values=["80%", "90%", "100%", "110%", "120%"], command=self.UiScaling)
        uiScale.grid(row=1,column=0, padx=20, pady=20, sticky="n")
        btnExport = ctk.CTkButton(widgetmenu,corner_radius=8,text="export all values to txtFile", command=self.export_to_txt)
        btnExport.grid(row=2,column=0,pady=20,padx=20)

        # Main menu frame
        mainmenu = ctk.CTkFrame(self.root1, height=750, width=1225, corner_radius=8)
        mainmenu.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        lblWelcome = ctk.CTkLabel(mainmenu, corner_radius=8,width=1,height=50,text="Lachlans Crypto Scraper", font=ctk.CTkFont(family='Arial', size=40))
        lblWelcome.grid(row=0,column=0,padx=20, pady=20)
        lblMessage = ctk.CTkLabel(mainmenu, corner_radius=8,width=50,height=50,text="All Graphs in AUD", font=ctk.CTkFont(family='Arial', size=10))
        lblMessage.grid(row=0,column=1,padx=20, pady=20)
        btnBitcoin = ctk.CTkLabel(mainmenu, corner_radius=8,text=f"{self.lista[0]}, Currency: {self.lista[1] * int(usdToAud) }", width=300)
        btnBitcoin.grid(row=1,column=0,padx=20, pady=20, sticky="n")
        btnLitecoin = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[2]}, Currency: {self.lista[3]}", width=300)
        btnLitecoin.grid(row=2,column=0,padx=20, pady=20)
        btnEthereum = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[4]}, Currency: {self.lista[5]}", width=300)
        btnEthereum.grid(row=3,column=0,padx=20, pady=20)
        btnSolana = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[6]}, Currency: {self.lista[7]}",width=300)
        btnSolana.grid(row=4,column=0,padx=20, pady=20)
        btnSyscoin = ctk.CTkLabel(mainmenu,corner_radius=8,text=f"{self.lista[8]}, Currency: {self.lista[9]}", width=300)
        btnSyscoin.grid(row=5,column=0,padx=20, pady=20)
        btnGraph1 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[0]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[0])))
        btnGraph1.grid(row=1,column=1,padx=20, pady=20, sticky="n")
        btnGraph2 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[2]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[2])))
        btnGraph2.grid(row=2,column=1,padx=20, pady=20, sticky="n")
        btnGraph3 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[4]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[4])))
        btnGraph3.grid(row=3,column=1,padx=20, pady=20, sticky="n")
        btnGraph4 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[6]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[6])))
        btnGraph4.grid(row=4,column=1,padx=20, pady=20, sticky="n")
        btnGraph5 = ctk.CTkButton(mainmenu,corner_radius=8, text=f"Show {self.lista[8]} Graph", command=lambda: Graph(crypto_dict.get(self.lista[8])))
        btnGraph5.grid(row=5,column=1,padx=20, pady=20, sticky="n")

        #Footer
        Footer = ctk.CTkFrame(self.root1, height=300, width=1225, corner_radius=8)
        Footer.grid(row=4, column=1,padx=20, pady=20, sticky="n")
        lblConnection = ctk.CTkLabel(Footer,corner_radius=8,text=f"{self.ConnectionSate(url = "https://crypto.com/price")}", width=880,font=ctk.CTkFont(family='Arial', size=40))
        lblConnection.grid(row=0,column=0,padx=20, pady=20, sticky="n")
        lblSelect = ctk.CTkLabel(Footer, corner_radius=8, text="If your are experiencing Issues, Please select Another Website.")
        lblSelect.grid(row=1,column=0,padx=20, pady=5, sticky="n")
        lblSelect2 = ctk.CTkLabel(Footer, corner_radius=8, text="Warning. If you switch Website, The displayed cryptos may change.")
        lblSelect2.grid(row=2,column=0,padx=20, pady=5, sticky="n")
        cbxWebsite = ctk.CTkComboBox(Footer,corner_radius=9, values= ['Coinspot', 'Crypto.com'], command= self.CheckCBX)
        cbxWebsite.set("Crypto.com")
        cbxWebsite.grid(row=3,column=0,padx=20, pady=5, sticky="n")


        self.root1.mainloop() 
    def CheckCBX(self, cbx):
        if cbx == 'Coinspot':
            self.root1.destroy()
            App()
        

    #Theme Change Function
    def changeTheme(self, choice):  
        if choice == "Dark Mode":
            ctk.set_appearance_mode("dark")
        elif choice == "Light Mode":
            ctk.set_appearance_mode("light")  

    #UI Scaling Function
    def UiScaling(self, scalingValue):
        match scalingValue:
            case "80%":
                ctk.set_widget_scaling(0.8)
            case "90%":
                ctk.set_widget_scaling(0.9)
            case "100%":
                ctk.set_widget_scaling(1.0)
            case "110%":
                ctk.set_widget_scaling(1.1)
            case "120%":
                ctk.set_widget_scaling(1.2)
    # Export current top cryptos and their values to txt File
    def export_to_txt(self):
        date = datetime.today().strftime('%d-%m-%Y')
        #Using the default extension to default it to a txt file
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=f"{date} Cryptos")
        if file_path:
            #Opens file manager and asks where you would like to store the file
            with open(file_path, 'w') as file:
                for item in self.lista:
                    file.write(f"{item}\n")
            messagebox.showinfo("Export", "Data exported successfully!")
    
    def ConnectionSate(self, url):
        r = requests.head(url)
        if r.status_code == 200:
            print("Website up!")
            return "Website Up!"

    def crypto_details(self, url):
        URL = url
        response = requests.get(URL)
        print(response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class':'chakra-table css-1qpk7f7'})
        rows = table.find_all('tr', {'class': 'css-1cxc880'})

        self.lista = []

        for row in rows:
            name = row.find('p', {'class': 'chakra-text css-rkws3'})
            value = row.find('p', {'class': 'chakra-text css-13hqrwd'})
            if name and value:
                print(f"Name: {name.text.strip()}, Value: {value.text.strip()}")
                self.lista.append(name.text.strip())
                self.lista.append(value.text.strip())

if __name__ == "__main__":
    frmLogin()


class CCUser:
    def __init__(self, db_name: str = "User.Db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.CreateTable()
        self.Insert("John55", "hi")  
        self.Login()

    def CreateTable(self):
        """Create the user table."""
        self.cursor.execute("DROP TABLE IF EXISTS tblUser")
        self.conn.commit()
        self.cursor.execute(
            "CREATE TABLE tblUser (Username VARCHAR UNIQUE, Password TEXT)"
        )
        self.conn.commit()

    def Insert(self, username, password):
        """Insert a user with a hashed password."""
        try:
            hashedpw = self.HashInput(password)
            query = "INSERT INTO tblUser (Username, Password) VALUES (?, ?)"
            self.cursor.execute(query, (username, hashedpw))
            self.conn.commit()
            print(f"Inserted user '{username}' with hashed password: {hashedpw}")
        except sqlite3.Error as e:
            print(f"Unable to insert: {e}")

    def Search(self, username):
        """Search for the user by username and return the password hash."""
        query = "SELECT Password FROM tblUser WHERE Username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        self.conn.commit()
        return result

    def Login(self):
        """Prompt the user for login and verify their credentials."""
        username = input("\nUsername: ")
        password = input("Password: ")

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




