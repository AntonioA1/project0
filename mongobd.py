from pymongo import MongoClient
from tabulate import tabulate
from validatation import shirt, get_units

client = MongoClient('localhost:27017')
db = client.acc
ledger = db.Ledger
inv = db.Inv_Shirts
cust = db.Customers

def cash_sale():
    item_id = shirt()
    units = get_units()
    item = inv.find_one({"_id" : item_id})
    price = item['Price']
    cost = item['Cost']
    amount = units*price
    cogs = units*cost
    doc = [{"Account" : "Cash", "Debit" : amount, "Credit" : 0},
            {"Account" : "Revenue", "Debit" : 0, "Credit" : amount},
            {"Account" : "COGS", "Debit" : cogs, "Credit" : 0},
            {"Account" : "Inventory", "Debit" : 0, "Credit" : cogs}]
    ledger.insert_many(doc)

def credit_sale():
    print("\nPlease select item, customer and input quantity: \n")
    item_id = shirt()
    units = get_units()
    item = inv.find_one({"_id" : item_id})    
    customer_id = input("\tPlease enter customer id (C1, C2, C3, C4 or C5): ")
    if customer_id in ['C1', 'C2', 'C3', 'C4', 'C5']:
        customer = cust.find_one({"_id" : customer_id})  
        cust_name = customer['Name']  
        price = item['Price']
        cost = item['Cost']
        amount = units*price
        cogs = units*cost
        doc = [{"Account" : "Accounts Receivables", "Debit" : amount, "Credit" : 0, "name" : cust_name},
                {"Account" : "Revenue", "Debit" : 0, "Credit" : amount},
                {"Account" : "COGS", "Debit" : cogs, "Credit" : 0},
                {"Account" : "Inventory", "Debit" : 0, "Credit" : cogs}]
        ledger.insert_many(doc)
        print("\nTransaction was recorded succesfully!")
    else:
        print("\nTransaction was not recorded!")

def cash_purchase():
    print("\nPlease select item and input quantity: \n")
    item_id = shirt()
    units = get_units()
    item = inv.find_one({"_id" : item_id})
    cost = item['Cost']
    amount = units*cost    
    doc = [{"Account" : "Inventory", "Debit" : amount, "Credit" : 0},
            {"Account" : "Cash", "Debit" : 0, "Credit" : amount}]
    ledger.insert_many(doc)

def credit_purchase():
    print("\nPlease select item and input quantity: \n")
    item_id = shirt()
    units = get_units()
    item = inv.find_one({"_id" : item_id})    
    supplier = item['Supplier']
    supp_name = supplier['Name']  
    cost = item['Cost']
    amount = units*cost    
    doc = [{"Account" : "Inventory", "Debit" : amount, "Credit" : 0},
            {"Account" : "Accounts Payable", "Debit" : 0, "Credit" : amount, "name" : supp_name}]
    ledger.insert_many(doc)

def owner_deposit():
    amount = get_units() 
    doc = [{"Account" : "Cash", "Debit" : amount, "Credit" : 0},
            {"Account" : "Owners Equity", "Debit" : 0, "Credit" : amount}]
    ledger.insert_many(doc)

def owner_withdrawal():
    amount = get_units()  
    doc = [{"Account" : "Owners Equity", "Debit" : amount, "Credit" : 0},
            {"Account" : "Cash", "Debit" : 0, "Credit" : amount}]
    ledger.insert_many(doc)
    
def receivables():
    name = input("\nPlease enter customer Name: ")
    amount = get_units()
    doc = [{"Account" : "Cash", "Debit" : amount, "Credit" : 0},
            {"Account" : "Accounts Receivable", "Debit" : 0, "Credit" : amount, "name" : name}]
    ledger.insert_many(doc)

def payables():
    name = input("\nPlease enter supplier Name: ")
    amount = get_units()
    doc = [{"Account" : "Accounts Payable", "Debit" : amount, "Credit" : 0, "name" : name},
            {"Account" : "Cash", "Debit" : 0, "Credit" : amount}]
    ledger.insert_many(doc)

def view_ledger():
    x = []
    for docs in ledger.find({}, {'_id': False}):
        y = docs
        x.append(y)
    print("\n"+tabulate(x, headers="keys"))

def upsert_cust():
    name = input("\nPlease enter customer Name: ")
    cust_id = input("\nPlease enter customer id: ")
    filter = { '_id': cust_id }
    newvalues = { "$set": { 'Name': name } }
    cust.update_one(filter, newvalues, upsert=True)

def view_cust():
    x = []
    for docs in cust.find():
        y = docs
        x.append(y)
    print("\n"+tabulate(x, headers="keys"))

def delete_cust():
    name = input("\nPlease enter customer Name: ")
    cust.delete_one({"Name" : name})

#if __name__ == "__main__":
#    view_ledger()

# for coll in db.list_collection_names():
#     print(coll)

# vaina = coll.find()
# for doc in vaina:
#     print(doc)

