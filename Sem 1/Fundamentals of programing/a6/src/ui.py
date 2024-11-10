from datetime import datetime

OPERATION=0
INSERT_DAY=1
DAY=1
OPERATION_TYPE=1
ADD_OPERATION_VALUE=1
ADD_OPERATION_TYPE=2
VALUE=2
LINKING_WORD=2
INSERT_VALUE=2
FILTER_OPERATION_TYPE=2
INSERT_TYPE=3
REPLACE_AMMOUNT=4
LINKING_WORD_2=4
OPERATION_TYPES=['in','out']

def print_help_menu():
    help_text = """
1.add <value:int> <type:in/out> <description>
2.insert <day:int> <value:int> <type:in/out> <description>
3.remove <day:int>
4.remove <start day:int> to <end day:int>
5.remove <type:in/out>
6.replace <day:int> <type:in/out> <description> with <value:int>
7.list
8.list <type:in/out>
9.list [ < | = | > ] <value:int>
10.list balance <day:int>
11.filter <type:in/out>
12.filter <type:in/out> <value:int>
13.undo-undo last command
14.exit-exit the program
"""
    print(help_text)
def undo_error():
    print("No more commands to undo")

def print_error(error):
    print(f"Something went wrong,try again\n{error}")

def user_input_valid(user_input: str):
    user_input_list = user_input.split(sep=' ')
    command_word_count = len(user_input_list)

    if command_word_count == 1 and (user_input_list[OPERATION] in ['help', 'list', 'undo', 'exit']):
        return True

    if user_input_list[OPERATION] == 'list':
        if command_word_count == 1:
            return True
        if command_word_count==2:
            if user_input_list[OPERATION_TYPE] in OPERATION_TYPES:
                return True
            else:
                print("Operation type not valid,try in/out")
                return False
        if command_word_count==3:
            if user_input_list[OPERATION_TYPE] in ['<', '=', '>', 'balance']:
                try:
                    number=int(user_input_list[VALUE])
                    if user_input_list[OPERATION_TYPE] == 'balance':
                        if number < 1 or number > 30:
                            print("Day not in range")
                            return False
                    return True
                except ValueError :
                    print("Number not valid")
                    return False
            else:
                print("Value not valid,try <,=,> or balance")
                return False
        else:
            print("Form of command not correct")
            return False
    if user_input_list[OPERATION] == 'filter':
        if command_word_count == 2:
            return True
        if command_word_count == 3 and user_input_list[FILTER_OPERATION_TYPE] in OPERATION_TYPES:
            try:
                number = int(user_input_list[VALUE])
                return True
            except ValueError:
                print("Form of command not correct")
                return False
        else:
            print("Form of command not correct")
            return False
    if user_input_list[OPERATION] == 'remove':
        if command_word_count == 2:
            if user_input_list[OPERATION_TYPE] in OPERATION_TYPES:
                return True
            else:
                try:
                    number = int(user_input_list[DAY])
                    if number < 1 or number > 30:
                        print("Day not in range")
                        return False
                    return True
                except ValueError:
                    print("Form of command not correct")
                    return False
        if command_word_count == 4 and user_input_list[LINKING_WORD] == 'to':
            try:
                number = int(user_input_list[LINKING_WORD + 1])
                number = int(user_input_list[LINKING_WORD - 1])
                return True
            except ValueError:
                print("Form of command not correct")
                return False
        else:
            print("Form of command not correct")
            return False
    if user_input_list[OPERATION] == 'replace':
        if command_word_count == 5 and user_input_list[LINKING_WORD_2] == 'with' and user_input_list[OPERATION_TYPE+1] in OPERATION_TYPES:
            try:
                number = int(user_input_list[DAY])
                if number < 1 or number > 30:
                    print("Day not in range")
                    return False
                number = int(user_input_list[REPLACE_AMMOUNT])
                return True
            except ValueError:
                print("Form of command not correct")
                return False
        else:
            print("Form of command not correct")
            return False
    if user_input_list[OPERATION] == 'add':
        if command_word_count == 4 and user_input_list[ADD_OPERATION_TYPE] in OPERATION_TYPES:
            try:
                number = int(user_input_list[ADD_OPERATION_VALUE])
                return True
            except ValueError:
                print("Form of command not correct")
                return False
        else:
            print("Form of command not correct")
            return False
    if user_input_list[OPERATION] == 'insert':
        if command_word_count == 5 and user_input_list[INSERT_TYPE] in OPERATION_TYPES:
            try:
                day = int(user_input_list[DAY])
                if day < 1 or day > 30:
                    print("Day not in range")
                    return False
                int(user_input_list[INSERT_VALUE])
                return True
            except ValueError:
                print("Form of command not correct")
                return False
        else:
            print("Form of command not correct")
            return False

    print("No such command")
    return False

def UI(account: object):
    account_history = list()
    account_history.append(account.copy())
    while True:
        try:
            print(f"Current day is {datetime.now().day}")
            user_input = input(">")
            if user_input_valid(user_input):
                user_input=user_input.split(sep=' ')
                if user_input[OPERATION] == 'add':
                    account.add_transaction(int(user_input[ADD_OPERATION_VALUE]), user_input[ADD_OPERATION_TYPE], user_input[INSERT_TYPE])
                    account_history.append(account.copy())
                elif user_input[OPERATION] == 'insert':
                    day = int(user_input[DAY])
                    insert_value = int(user_input[INSERT_VALUE])
                    insert_type = user_input[INSERT_TYPE]
                    description = user_input[insert_type + 1]
                    account.insert_transaction(day, insert_value, insert_type, description)
                    account_history.append(account.copy())
                elif user_input[OPERATION] == 'remove':
                    if len(user_input) == 2:
                        try:
                            day= int(user_input[DAY])
                            account.remove_transaction(day)
                            account_history.append(account.copy())
                        except ValueError:
                            account.remove_transaction_type(user_input[OPERATION_TYPE])
                            account_history.append(account.copy())
                    else:
                        start_day = int(user_input[LINKING_WORD - 1])
                        end_day = int(user_input[LINKING_WORD + 1])
                        account.remove_transaction_range(start_day, end_day)
                        account_history.append(account.copy())
                elif user_input[OPERATION] == 'replace':
                    day = int(user_input[DAY])
                    replace_ammount = int(user_input[REPLACE_AMMOUNT])
                    replace_type = user_input[OPERATION_TYPE]
                    replace_description = user_input[LINKING_WORD_2 - 1]
                    account.replace_transaction(day, replace_type, replace_description, replace_ammount)
                    account_history.append(account.copy())
                elif user_input[OPERATION] == 'list':
                    if len(user_input) == 1:
                        print(account)
                    elif len(user_input) == 2:
                        print(account.list_type(user_input[OPERATION_TYPE]))
                    elif len(user_input) == 4:
                        if user_input[OPERATION_TYPE] in ['<', '=', '>']:
                            input_operator = user_input[OPERATION_TYPE]
                            input_value = int(user_input[VALUE])
                            print(account.list_value(input_operator, input_value))
                    elif user_input[OPERATION_TYPE] == 'balance':
                        input_day = int(user_input[VALUE])
                        print(account.list_balance(input_day))
                elif user_input[OPERATION] == 'filter':
                    if len(user_input) == 2:
                        operation_type = user_input[OPERATION_TYPE]
                        account.filter_type(operation_type)
                        account_history.append(account.copy())
                    elif len(user_input) == 3:
                        operation_type = user_input[OPERATION_TYPE]
                        value = int(user_input[VALUE])
                        account.filter_value(operation_type, value)
                        account_history.append(account.copy())
                elif user_input[OPERATION] == 'undo':
                    if len(account_history) > 1:
                        account_history.pop()
                        account = account_history[-1]
                    else:
                        undo_error()
                elif user_input[OPERATION] == 'help':
                    print_help_menu()
                elif user_input[OPERATION]=='exit':
                    break
        except ValueError or Exception as error:
            print_error(error)