import json
# from typing import TextIO
import csv
from os import SEEK_SET
import datetime

WEARS_INDEX = 1
QTY_INDEX = 2
PRICE_INDEX = 3

        
def get_year()-> int:
    return datetime.datetime.now().year 


def update_qty(hub: list, choice: str)-> None:
    for item in hub:
        if choice == item[1]:
            item[2] -= 1
            
def update_price(data: dict, style: str, price: float) -> None:
    # data[style] = data.setdefault(style, 0) + price
      data[style] = data.get(style, 0) + price
      

def parse_invoice_number(invoice_number: str) -> tuple[int, int]:
    """Split a well-formed invoice "number" into its component parts. 
    """
    year, number = invoice_number.split('-')
    return int(year), int(number)


def next_invoice_number(invoice_number: str) -> str:
   
    invoice_year, number = parse_invoice_number(invoice_number)
    year = get_year()
    if year == invoice_year:
        number += 1
    else:
        invoice_year = year
        number = 1
    next_invoice_number = f'{invoice_year}-{number:04d}'
    return next_invoice_number

      
filename = 'shopping_list.json'
with open(filename,'r+', encoding= 'utf-8') as shoppers:
    site = json.load(shoppers)

stock = {}
stock_2 = {}
cart = {}
record = []
 

while True:
    print('Welcome to wears.com ')
    print('\tPlease select your choice of brand: ')
    for key,values in enumerate(site, start=1):
        print(key, values)
        stock[str(key)] = values
        
    choice = input(f'\tselect a brand to buy from: ')

    if choice in stock:
        chosen = stock[choice]
        # print(site[chosen])
        selection = site[chosen]
        for key, values in enumerate(selection, start=1):
            print(key, values)
            stock_2[str(key)] = values
            
    choice = input('Select choice of wears: ')        
    if choice in stock_2: 
        chosen = stock_2[choice]
        selected_wear = selection[chosen]
        print(selected_wear)    

    choice = input('select your wears: ')
    if 1 <= int(choice) <= 3:        
        chosen_wear = selected_wear[int(choice)-1][WEARS_INDEX]
        record.append(chosen_wear)         
        new_record = set(record)
        wears_price = selected_wear[int(choice)-1][PRICE_INDEX]
        # Updating quantity helps to reduce amount posted as each item is being selected
        update_qty(selected_wear,chosen_wear)  
        # Passing price upate helps to increment price as a product is selected multiple times
        update_price(cart,chosen_wear,wears_price)  
        # Using d combination of a list and a set will help keep record of each selected item and increment 
        # as selection increases
        for item in new_record:
            if item in record:
               print(f"{item}: {record.count(item)}")  
        for product, price in cart.items():
            print(f'{product} is ${price}')          
  
    with open(filename,'w', encoding= 'utf-8') as shoppers:
        json.dump(site, shoppers)
        
    filename = 'record_invoice.csv'    
    with open(filename, 'w', encoding='utf-8', newline='') as output_file:        
        writer = csv.writer(output_file)         
        headers = ['Invoice_Number/Year', 'Item', 'Amount'] 
        writer.writerow(headers)
        transaction = []
        for product, price in cart.items():
                year = get_year()
                invoice_num = 1
                new_invoice = f'{year}-{invoice_num:04d}'
                transaction.append([new_invoice, product, price])                    
        writer.writerows(transaction)
        
        
        
    with open(filename, 'r+', encoding='utf-8', newline='') as output_file:
        reader = csv.reader(output_file)
        lastline = ''
        for row in reader:
            lastline = row
            
        if lastline:            
            invoice_number = lastline[0]                   
            new_invoice = next_invoice_number(invoice_number)            
        else: 
            invoice_year = get_year()
            invoice_no = 1
            new_invoice = f'{invoice_year}-{invoice_no:04d}'
        
        for product,price in cart.items():
            transaction = [new_invoice,product,price]
        writer = csv.writer(output_file)
        writer.writerow(transaction)
        
            
        
      


            
        
                
                
             
  