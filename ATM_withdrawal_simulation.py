
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pyzipcode import ZipCodeDatabase
from PIL import Image, ImageTk
import pytz
import datetime
import csv
from os import SEEK_SET
import os
import pymysql


zcdb = ZipCodeDatabase()
local_time = datetime.datetime.now()
time_now = pytz.utc.localize(local_time)
date_time = str(time_now)[:-13]

class Register(ttk.Frame):
    @classmethod      
    def verify(cls):   
        filename = 'customer_data.csv'
        with open(filename, 'r', encoding='utf-8', newline='') as customer_data:             
            reader = csv.DictReader(customer_data, delimiter='\t')            
            val = [] 
            user = []
            cls.ent_data = {}                 
            for row in reader:                 
                val.append([row['FirstName'], row['LastName'], row['Username'], row['Password']]) 
                user.append([row['Username'], row['Password']]) 
                cls.fname = row['FirstName']
                cls.lname = row['LastName']
                cls.usern = row['Username']
                cls.ent_data[row['Username']] = row                 
        cls.data = val[:] 
        cls.data_l = user[:]
                                            

    def create_label_frame(cls, parent, text, rol, col):
        label = tk.LabelFrame(parent,text=text, background='green', fg='white')
        label.grid(row=rol, column=col, sticky='ew', padx=10, pady=10)
        return label       
      
    def create_label(cls,parent, text, rol, col):
        label = ttk.Label(parent,text=text)
        label.grid(row=rol, column=col, sticky='nsew', padx=10, pady=10)
        return label  
   
    def create_combobox(cls, parent, values, rol, col):
        """Create and return a Combobox widget."""
        combobox = ttk.Combobox(parent, values=values)
        combobox.grid(row=rol, column=col, padx=10, pady=10, sticky='nsew')
        return combobox
    
    def create_spinbox(cls, parent, from_, to, rol, col):
        """Create and return a Spinbox widget."""
        spinbox = ttk.Spinbox(parent, from_=from_, to=to)
        spinbox.grid(row=rol, column=col, padx=10, pady=10, sticky='nsew')
        return spinbox      
      
    def create_entry(cls,parent, rol, col,val):
        entry = ttk.Entry(parent, show=val)
        entry.grid(row=rol, column=col, sticky='nsew', padx=10, pady=10)
        return entry     

    def get_states(cls):
        """Get the list of states from ZipCodeDatabase."""
        return sorted(set([value.state for _, value in zcdb.items()])) 

    def get_cities(cls):
        """Get the list of cities from ZipCodeDatabase."""
        return sorted(set([value.city for _, value in zcdb.items()]))                

    def __init__(self):
        super().__init__()        
        self.verify()
        self.FN = self.fname
        self.LN = self.lname
        self.E = self.usern

    def set_name(self, fname, lname, usern):
        self.FN = fname
        self.LN = lname
        self.E = usern             
        
    def gui(self):

        self.b_image = Image.open(".//second_page.jpeg")
        self.b_image = self.b_image.resize((1920, 1200), Image.Resampling.LANCZOS)
        self.b_image = ImageTk.PhotoImage(self.b_image)  
             
        self.pack(expand=True, fill='both', padx=5, pady=5)        

        self.frame = ttk.Label(self,image=self.b_image)
        self.frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.frame.rowconfigure(0, weight=1, uniform='a')
        for widget in self.frame.winfo_children():
            widget.grid_configure(padx=5, pady=5, columnspan=1)  

        # user information
        label_frame = self.create_label_frame(self.frame, 'User Information', 0, 0)  
        for col in range(3):
            label_frame.columnconfigure(col, weight=1) 
        for widget in label_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5, columnspan=3)          

        label = self.create_label(label_frame, 'First Name:', 0, 0)
        self.fname = self.create_entry(label_frame, 1, 0,'show')
        label = self.create_label(label_frame, 'Last Name:', 0, 1)        
        self.lname = self.create_entry(label_frame, 1, 1, 'show')
        label = self.create_label(label_frame, 'Title: ', 0, 2)
        self.title = self.create_combobox(label_frame, ['Mr', 'Mrs', 'Miss', 'Dr'], 1, 2)
        label = self.create_label(label_frame, 'Age: ', 2, 0)
        self.age = self.create_spinbox(label_frame, 18, 65, 3, 0)
        label = self.create_label(label_frame, 'Race: ', 2, 1)
        self.race = self.create_combobox(label_frame, ['Africa/American', 'Caucasian', 'Latino', 'Asian'], 3, 1)
        label = self.create_label(label_frame, 'Gender: ', 2, 2)
        self.gender = self.create_combobox(label_frame, ['M', 'F'], 3, 2)

        # login information
        label_frame = self.create_label_frame(self.frame, 'Login Information', 1, 0)  
        # label_frame.rowconfigure((0), weight=1)
        label_frame.columnconfigure((0,1), weight=1) 
        for widget in label_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5, columnspan=2)

        label = self.create_label(label_frame, 'Username: ', 0, 0)
        self.username = self.create_entry(label_frame, 1, 0,'show')
        label = self.create_label(label_frame, 'Password: ', 0, 1)
        self.password = self.create_entry(label_frame, 1, 1,'*')
        
        # contact information
        label_frame = self.create_label_frame(self.frame, 'Contact Information', 2, 0)         
        for widget in label_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5, columnspan=3)

        # state city address cell phone, zipcode
        label = self.create_label(label_frame, 'State', 0, 0)        
        self.states = self.create_combobox(label_frame, [], 1, 0)
        label = self.create_label(label_frame, 'City', 0, 1)
        self.city = self.create_combobox(label_frame, [], 1, 1)
        label = self.create_label(label_frame, 'Address: ', 0, 2)
        self.address = self.create_entry(label_frame, 1, 2,'show')
        label = self.create_label(label_frame, 'Zipcode', 2, 0)
        self.zipcode = self.create_entry(label_frame, 3, 0, 'show')
        label = self.create_label(label_frame, 'Cell Phone', 2, 1)
        self.cellphone = self.create_entry(label_frame, 3, 1,'show')

        # complete form
        submit_btn = ttk.Button(label_frame, text='Submit', command=self.on_submit)
        next_btn = ttk.Button(label_frame, text='Next', command= self.close_interface)
        submit_btn.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        next_btn.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')

    def on_submit(self):        
        self.firstnamE = self.fname.get()
        self.lastnamE = self.lname.get()
        self.titlE = self.title.get()
        self.agE = self.age.get()
        self.racE = self.race.get()
        self.gendeR = self.gender.get()
        self.usernamE = self.username.get()
        self.passworD = self.password.get()
        self.stateS = self.states.get()
        self.citY = self.city.get()
        self.addresS = self.address.get()
        self.zipcodE = self.zipcode.get()
        self.cellphonE = self.cellphone.get() 
        
        # this is a list comprehension that validates if a user has an existing record
        # to avoid duplication of records
        value = [(self.firstnamE,self.lastnamE,self.usernamE) for f,l,u in self.data
                  if self.firstnamE == f and self.lastnamE == l and self.usernamE == u]        
        if value:
                tk.messagebox.showerror('Duplicate', 'Duplicate entry')
        elif not self.firstnamE:
            tk.messagebox.showinfo('blank', 'first name can not be null')        
        elif not self.lastnamE:
            tk.messagebox.showinfo('blank', 'last name can not be null')  
        elif not self.agE:
            tk.messagebox.showinfo('blank', 'age can not be null')  
        elif not self.gendeR:
            tk.messagebox.showinfo('blank', 'gender can not be null')
        elif not self.usernamE:
            tk.messagebox.showinfo('blank', 'username can not be null')
        elif not self.passworD:
            tk.messagebox.showinfo('blank', 'password can not be null')
        elif not self.titlE:
            tk.messagebox.showinfo('blank', 'title can not be null')
        elif not self.addresS:
            tk.messagebox.showinfo('blank', 'address can not be null')
        elif not self.cellphonE:
            tk.messagebox.showinfo('blank', 'cellphone can not be null')
        elif not self.zipcodE:
            tk.messagebox.showinfo('blank', 'zipcode can not be null')
        elif not self.citY:
            tk.messagebox.showinfo('blank', 'city can not be null')
        elif not self.stateS:
            tk.messagebox.showinfo('blank', 'state can not be null')

        else:
            self.save_data()
            self.close_interface()

    def save_data(self):
        tk.messagebox.showinfo('Success', f'Welcome {self.firstnamE}')
        
        filename = 'customer_data.csv'
        if os.path.exists(filename):
            with open(filename, 'a', encoding='utf-8', newline='') as output_file:
                writer = csv.writer(output_file, delimiter="/")
                writer.writerow([self.firstnamE, self.lastnamE, self.titlE, self.agE, self.racE, self.gendeR,
                                 self.usernamE, self.passworD, self.stateS, self.citY, self.addresS, self.cellphonE])                
        else:
            with open(filename, 'r+', encoding='utf-8', newline='') as output_file:
                writer = csv.writer(output_file, delimiter='\t')
                header = ['FirstName', 'LastName', 'Title', 'Age', 'Race', 'Gender', 
                        'Username', 'Password', 'State', 'City', 'Address', 'Cellphone']                
                writer.writerow(header)
                writer.writerow([self.firstnamE, self.lastnamE, self.titlE, self.agE, self.racE, self.gendeR,
                                 self.usernamE, self.passworD, self.stateS, self.citY, self.addresS, self.cellphonE])

    def close_interface(self):
        self.pack_forget()       
        self.parent = ttk.Label(self).pack(expand=True, fill='both', padx=10, pady=10)
        lg = Login(self.parent)
        lg.gui()
        lg.mainloop()


class Login(Register):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

    def gui(self):
        self.bgimage = Image.open(".//home_page.jpeg")
        self.bgimage = self.bgimage.resize((1200, 800), Image.Resampling.LANCZOS)
        self.bgimage = ImageTk.PhotoImage(self.bgimage)

        self.pack(expand=True, fill='both', padx=10, pady=10)        

        self.fr = ttk.Label(self, image=self.bgimage)
        self.fr.pack(expand=True, fill='both', padx=10, pady=10)
        # self.fr.columnconfigure((3), weight=1)
        # self.fr.rowconfigure((0), weight=1)

        self.lframe = self.create_label_frame(self.fr, "Login Page", 0, 0)

        # self.lframe.rowconfigure(3, weight=1)
        # self.lframe.columnconfigure((0), weight=1)
        ulabel = self.create_label(self.lframe, "Username: ", 0, 0)
        self.lusername_entry = self.create_entry(self.lframe, 1, 0, None)
        plabel = self.create_label(self.lframe, 'Password: ', 2, 0)
        self.lpassword_entry = self.create_entry(self.lframe, 3, 0,'*')  
        submit_bttn = ttk.Button(self.lframe, text='Submit', command= self.validate)
        submit_bttn.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')        

    def validate(self):
        # self.submit()
        username = self.lusername_entry.get()
        password = self.lpassword_entry.get()

        if username in self.ent_data:
                self.fname = self.ent_data[username]['FirstName']
                self.lname = self.ent_data[username]['LastName']
                self.user = self.ent_data[username]
                self.set_name(self.fname, self.lname, username)
        else:
            print('not found')
        value = [(username, password) for u,p in self.data_l if username == u and password == p]        
        if value:
            self.submit()
        else:
            tk.messagebox.showerror('Invalid', f'Invalid login details')

    def submit(self): 
        tk.messagebox.showinfo('Success', f'Welcome to {self.FN}')       
        self.destroy()
        bank = BankAccount(self.fname, self.lname)
        bank.account_gui()
        bank.mainloop()     


class BankAccount(Register):
    @classmethod
    def account(cls):
        try:
            filename = 'customer_balance.csv'
            cls.detail ={}   
            data_key = ['firstname', 'lastname', 'balance', 'history']         
            with open(filename, 'r', encoding='utf-8', newline='') as output_data:
                output_data.readline()
                reader = csv.DictReader(output_data, delimiter='\t', fieldnames=data_key)
                for row in reader:
                    if row:  
                        cls.detail[row['firstname']] = row  
                          
        except FileNotFoundError:
            print('Cannot locate file')
        except KeyError:
            print('could not find keys')

    def __init__(self, fn, ln):
        super().__init__()
        self.FN = fn
        self.LN = ln
        self.account()  #from classmethod               
        self.balance = self.balanced()
        self.dtime = date_time               
        self.transaction_list = self.update_record()   
        self.text = tk.StringVar() 
        self.value = tk.StringVar()   

    def account_gui(self): 
        self.bg = Image.open(".//last_page.jpeg")
        self.bg = self.bg.resize((1200, 800), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.pack(expand=True, fill='both', padx=5, pady=5)

        self.mainframe = ttk.Label(self,image=self.bg)
        self.mainframe.pack(expand=True, fill='both', padx=10,pady=10)

        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure((0,1), weight=1)

        button_20_d = ttk.Button(self.mainframe, text='$20', command= lambda:self.deposit(20))
        button_20_d.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        button_40_d = ttk.Button(self.mainframe, text='$40', command= lambda:self.deposit(40))
        button_40_d.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        button_60_d = ttk.Button(self.mainframe, text='$60', command= lambda:self.deposit(60))
        button_60_d.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
        button_acct_blc = ttk.Button(self.mainframe, text='Account Blc', command= self.account_info)
        button_acct_blc.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')        
        
        button_deposit = ttk.Button(self.mainframe, text='Deposit', command=lambda:self.manual_deposit())
        button_deposit.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')        
        
        self.display_lab = ttk.Label(self.mainframe, background='white', foreground='black', textvariable=self.text)
        self.display_lab.grid(row=0, rowspan=5, column=1, columnspan=3, padx=5, pady=5, sticky='nsew')      

        button_20_w = ttk.Button(self.mainframe, text='$20', command=lambda:self.withdraw(20))
        button_20_w.grid(row=0, column=4, padx=5, pady=5, sticky='nsew')

        button_40_w = ttk.Button(self.mainframe, text='$40', command= lambda:self.withdraw(40))
        button_40_w.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

        button_60_w = ttk.Button(self.mainframe, text='$60', command= lambda:self.withdraw(60))
        button_60_w.grid(row=2, column=4, padx=5, pady=5, sticky='nsew')

        button_withdraw = ttk.Button(self.mainframe, text='Withdraw', command=lambda:self.manual_withdraw())
        button_withdraw.grid(row=3, column=4, padx=5, pady=5, sticky='nsew')

        button_transaction_hist = ttk.Button(self.mainframe, text='Transaction History', command=self.transaction_history)
        button_transaction_hist.grid(row=4, column=4, padx=5, pady=5, sticky='nsew')
        
        label = ttk.Label(self.mainframe, text= 'Enter Amount')
        label.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

        self.entry = ttk.Entry(self.mainframe, textvariable=self.value)
        self.entry.grid(row=5, column=2, columnspan=3, sticky='ns', padx=5, pady=5)

        exit_button = ttk.Button(self.mainframe, text='Exit', command=self.destroy)
        exit_button.grid(row=6, column=0, padx=5, pady=5, sticky='ns')


    def balanced(self):
        return int(self.detail[self.FN]['balance']) if self.FN in self.detail else 0       

    def update_record(self): 
        self.transaction_list = []
        if self.FN in self.detail:
           return self.detail[self.FN]['history']        
        return self.transaction_list                     

    def account_info(self):
        if self.balance == 0:       
            message = f'Good Day {self.FN} {self.LN}, Your starting balance is ${self.balance}.00'
        else:
            message = f'Good Day {self.FN} {self.LN}, Your balance is ${self.balance}.00'

        self.text.set(value=message)        
        return self.text

    def withdraw(self, amount):
        if self.balance < amount:
            message = f'Insufficient fund'
        elif self.balance >= amount:
            self.balance -= amount            
            message = f'Withdrawal alert! Your current balance is ${self.balance}.00'
            self.text.set(value=message)
            self.transaction_list.append((self.FN,self.dtime,f'-${amount}',message))
        self.text.set(value= message)

    def deposit(self, amount):
        self.balance += amount        
        message = f'Deposit alert! Your current balance is ${self.balance}.00'
        self.transaction_list.append((self.FN,self.dtime,f'+${amount}',message))
        self.text.set(value=message)

    def manual_deposit(self):
        try:
            amount = int(self.value.get())
            self.deposit(amount)
        except ValueError:
            message = "Invalid deposit"
            self.text.set(value=message) 

    def manual_withdraw(self):
        try:
            amount = int(self.value.get())
            self.withdraw(amount)
        except ValueError:
            message = "Invalid deposit"
            self.text.set(value=message)    

    # Join joins each string from the tuple on a new line
    def transaction_history(self):
        if self.transaction_list:
           history = '\n'.join([f'{t[0]} | {t[1]} | {t[2]} | {t[3]}' for t in self.transaction_list])            
        else: 
           history= 'No transaction history'   
        self.text.set(value=history)         
        return history

    def save_record(self):
        # Save transaction history and balance to a CSV file
        filename = 'customer_balance.csv'        
        record = self.transaction_history()    
        # Write or update the record in the CSV file
        try:
            if os.path.exists(filename):
                data = [self.FN, self.LN, self.balance,record]
                with open(filename, 'a', encoding='utf-8', newline='') as output_data:
                    writer = csv.writer(output_data, delimiter='\t')
                    writer.writerow(data)
            else:
                fieldns = ['firstname', 'lastname', 'balance', 'history']
                data = [self.FN, self.LN, self.balance,record]
                zipobj = zip(fieldns,data)
                with open(filename, 'w', encoding='utf-8', newline='') as output_data:
                    writer = csv.DictWriter(output_data, fieldnames=fieldns, delimiter='\t')
                    writer.writeheader()
                    writer.writerow(dict(zipobj)) 
                           
        except FileNotFoundError:
            print('Cannot locate file')
        except KeyError:
            print('Cannot read keys')

    def email_alert(self):
        pass

root = tk.Tk()
root.title("Home")
root.geometry('1200x800+150+50')

def init():    
    reg = Register()
    reg.gui()
    reg.mainloop()
