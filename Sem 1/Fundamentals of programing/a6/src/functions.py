from ui import undo_error
import datetime
import random

"""
command_history:
-type:list
-format:account at [i] command where i is the command number

account
-type: dictionary with key=day
-format:[amount:int,description:str]:tuple

John wants to manage his bank account. To do this, he needs an application to store all the bank transactions performed on his account during a month. Each transaction is stored in the application using the following elements: day (of the month in which the transaction was made, between 1 and 30 for simplicity), amount of money (transferred, positive integer), type (in - into the account, out – from the account), and description. Write a program that implements the functionalities exemplified below:

(A) Add transaction
add <value> <type> <description>
insert <day> <value> <type> <description>
e.g.
add 100 out pizza – add to the current day an out transaction of 100 RON with the "pizza" description
insert 25 100 in salary – insert to day 25 an in transaction of 100 RON with the “salary” description

(B) Modify transactions
remove <day>
remove <start day> to <end day>
remove <type>
replace <day> <type> <description> with <value>
e.g.
remove 15 – remove all transactions from day 15
remove 5 to 10 – remove all transactions between days 5 and 10
remove in – remove all in transactions
replace 12 in salary with 2000 – replace the amount for the in transaction having the “salary” description from day 12 with 2000 RON

(C) Display transactions having different properties
list
list <type>
list [ < | = | > ] <value>
list balance <day>
e.g.
list – display all transactions
list in – display all in transactions
list > 100 - display all transactions having an amount of money >100
list = 67 - display all transactions having an amount of money =67
list balance 10 – compute the account’s balance at the end of day 10. This is the sum of all in transactions, from which we subtract out transactions occurring before or on day 10

(D) Filter
filter <type>
filter <type> <value>
e.g.
filter in – keep only in transactions
filter in 100 – keep only in transactions having an amount of money smaller than 100 RON

(E) Undo
 – the last operation that modified program data is reversed. The user can undo all operations performed since program start by repeatedly calling this function.

Have at least 10 randomly generated items in your application at program startup

"""


VALUE=0
TYPE=1
DESCRIPTION=2
class Account:
    def __init__(self,num_transactions=10):
        self.account = {}
    def insert_transaction(self,day,value,transaction_type,description):
        if day not in self.account.keys():
            self.account[day] = []
        self.account[day].append([value,transaction_type,description])
    def add_transaction(self,value,transaction_type,description):
        day = datetime.datetime.now().day
        if day not in self.account.keys():
            self.account[day] = []
        self.account[day].append([value,transaction_type,description])
    def remove_transaction(self,day):
        if day in self.account.keys():
            del self.account[day]
    def remove_transaction_range(self,start_day,end_day):
        for day in range(start_day,end_day+1):
            if day in self.account.keys():
                del self.account[day]
    def remove_transaction_type(self,transaction_type):
        for day in self.account.keys():
            for transaction in self.account[day]:
                if transaction_type == transaction[DESCRIPTION]:
                    self.account[day].remove(transaction)
    def replace_transaction(self,day,transaction_type,description,value):
        for transaction in self.account[day]:
            if transaction_type == transaction[1] and description == transaction[DESCRIPTION]:
                transaction[VALUE] = value
    def copy(self):
        new_account = Account()
        for day in self.account.keys():
            for transaction in self.account[day]:
                new_account.add_transaction(transaction[VALUE],transaction[TYPE],transaction[DESCRIPTION])
        return new_account
    def __str__(self):
        string_account = ""
        for day in self.account.keys():
            string_account += "Day " + str(day) + ":\n"
            for transaction in self.account[day]:
                string_account += str(transaction[0]) + " " + str(transaction[1]) + " " + str(transaction[2]) + "\n"
        return string_account
    def list_type(self,transaction_type):
        string_account = ""
        for day in self.account.keys():
            for transaction in self.account[day]:
                if transaction_type == transaction[1]:
                    string_account += str(day) + " " + str(transaction[0]) + " " + str(transaction[1]) + " " + str(transaction[2]) + "\n"
        return string_account

    def list_value(self,sign,value):
        string_account = ""
        comparison = {'<':lambda x,y: x<y,'=':lambda x,y: x==y,'>':lambda x,y: x>y}
        for day in self.account.keys():
            for transaction in self.account[day]:
                if comparison[sign](transaction[0],value):
                    string_account += str(day) + " " + str(transaction[0]) + " " + str(transaction[1]) + " " + str(transaction[2]) + "\n"
        return string_account
    def list_balance(self,day):
        balance = 0
        for day in self.account.keys():
            for transaction in self.account[day]:
                if transaction[TYPE] == 'in':
                    balance += transaction[0]
                else:
                    if day <= day:
                        balance -= transaction[0]
        return balance
    def filter_type(self, transaction_category):
        for day in self.account.keys():
            for transaction in self.account[day]:
                if transaction_category != transaction[TYPE]:
                    self.account[day].remove(transaction)
    def filter_value(self, transaction_type, value):
        for day in self.account.keys():
            for transaction in self.account[day]:
                if transaction_type != transaction[TYPE] or transaction[VALUE] > value:
                    self.account[day].remove(transaction)