# Omer Schwartz 205486897
# Michael Hamami 204623375

from tkinter import *
import datetime
# import matplotlib.pyplot as plt
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('HW3_MichaelHamami_OmerSchwartz.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def print_date_before_function_call(func):
    def inner(*args, **kwargs):
        print(str(datetime.datetime.now()), end=" ")
        return func(*args, **kwargs)

    return inner


class Account:
    def __init__(self, name="", number=0, balance=0, credit_frame=1500):
        self.spent = 0
        self.name = name
        self.number = number
        self.balance = balance
        self.credit_frame = credit_frame

    def __str__(self):
        return "Name: " + str(self.name) + " Number: " + str(self.number) + " Balance: " + str(
            self.balance) + " Credit Frame: " + str(self.credit_frame) + " Transactions: "

    def __repr__(self):
        return f'({self.name, self.number, self.balance, self.credit_frame, self.transaction_lists})'

    def __eq__(self, other):
        if type(other) is Account and self.number == other.number:
            return True
        else:
            return False

    def deposit(self, amount_to_deposit):
        if type(amount_to_deposit) is not int:
            self.balance += int(amount_to_deposit)

    def withdraw(self, amount_to_withdraw):
        if type(amount_to_withdraw) is not int:
            amount_to_withdraw = int(amount_to_withdraw)
        if self.spent + amount_to_withdraw > self.credit_frame:
            return -1
        else:
            self.spent += amount_to_withdraw
            self.balance -= amount_to_withdraw
            return 1

    @print_date_before_function_call
    def transact_amount_to(self, account_to, amount_to_transact):
        if type(amount_to_transact) is not int:
            amount_to_transact = int(amount_to_transact)
        if self.spent + amount_to_transact > self.credit_frame:
            return -1
        else:
            self.spent += amount_to_transact
            self.balance -= amount_to_transact
            account_to.balance += amount_to_transact
            return 1


class TheBank:
    def __init__(self):
        self.account_list = []
        self.name = "Hamami & Schwartz Incorporate"

    def add_account_to_account_list(self, new_account):
        if new_account not in self.account_list:
            self.account_list.append(new_account)

    def get_accounts_balance(self):
        for account in self.account_list:
            yield account.balance

    def get_account_from_a_given_account_number(self, given_account_number):
        if type(given_account_number) is not int:
            given_account_number = int(given_account_number)
        for account in self.account_list:
            if account.number == given_account_number:
                return account
        return -1


class TkGui:

    def __init__(self, root):
        self.root = root
        self.row_index = 0
        # Handle Entries:
        self.entry_transaction_account_from = IntVar()
        self.transaction_amount_entry = IntVar()
        self.transaction_account_to_entry = IntVar()
        self.transaction_account_from_entry = IntVar()
        self.deposit_account_entry = IntVar()
        self.deposit_amount_entry = IntVar()
        self.withdraw_account_entry = IntVar()
        self.withdraw_amount_entry = IntVar()
        # Handle Labels:
        self.transaction_label = None
        self.transaction_amount_label = None
        self.transaction_account_to_label = None
        self.deposit_label = None
        self.deposit_amount_label = None
        self.withdraw_label = None
        self.withdraw_amount_label = None
        self.status_label = None
        self.updated_status_label = None
        # Handle Buttons:
        self.withdraw_button = None
        self.transaction_button = None
        self.deposit_button = None

    def update_gui(self, given_bank):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_accounts_details(given_bank)

        self.handle_transaction_widgets(given_bank)

        self.handle_deposit_widgets(given_bank)

        self.handle_withdraw_widgets(given_bank)

        self.handle_status_label()

    def show_accounts_details(self, given_bank):
        for account in given_bank.account_list:
            given_bank.account_name_label = Label(self.root, text="Account Name: " + str(account.name)).grid(
                row=self.row_index, column=1)
            given_bank.account_number_label = Label(self.root, text="Account Number: " + str(account.number)).grid(
                row=self.row_index + 1, column=1)
            given_bank.account_balance_label = Label(self.root, text="Account Balance: " + str(account.balance)).grid(
                row=self.row_index + 2, column=1)
            given_bank.account_credit_frame_label = Label(self.root,
                                                          text="Credit Frame: " + str(account.credit_frame)).grid(
                row=self.row_index + 3, column=1)
            given_bank.finish_account_label = Label(self.root,
                                                    text="-----------------------------------------------------").grid(
                row=self.row_index + 4, column=1)
            self.row_index += 5

    def handle_transaction_widgets(self, given_bank):
        self.row_index += 1
        self.transaction_label = Label(self.root, text="Transaction:  Account Number:").grid(row=self.row_index,
                                                                                             column=1)
        self.transaction_account_from_entry = Entry(self.root, textvar=self.transaction_account_from_entry)
        self.transaction_account_from_entry.grid(row=self.row_index, column=2)
        self.transaction_amount_label = Label(self.root, text="Amount: ").grid(row=self.row_index, column=3)
        self.transaction_amount_entry = Entry(self.root, textvar=self.transaction_amount_entry)
        self.transaction_amount_entry.grid(row=self.row_index, column=4)
        self.transaction_account_to_label = Label(self.root, text="Account To: ").grid(row=self.row_index,
                                                                                       column=5)
        self.transaction_account_to_entry = Entry(self.root, textvar=self.transaction_account_to_entry)
        self.transaction_account_to_entry.grid(row=self.row_index, column=6)
        self.transaction_button = Button(self.root, text="Commit Transaction",
                                         command=lambda: self.commit_transaction(given_bank)).grid(
            row=self.row_index, column=7)

    def handle_deposit_widgets(self, given_bank):
        self.row_index += 1
        self.deposit_label = Label(self.root, text="Deposit:  Account Number:").grid(row=self.row_index,
                                                                                     column=1)
        self.deposit_account_entry = Entry(self.root, textvar=self.deposit_account_entry)
        self.deposit_account_entry.grid(row=self.row_index, column=2)
        self.deposit_amount_label = Label(self.root, text="Amount: ").grid(row=self.row_index, column=3)
        self.deposit_amount_entry = Entry(self.root, textvar=self.deposit_amount_entry)
        self.deposit_amount_entry.grid(row=self.row_index, column=4)
        self.deposit_button = Button(self.root, text="Commit Deposit",
                                     command=lambda: self.commit_deposit(given_bank)).grid(
            row=self.row_index, column=7)

    def handle_withdraw_widgets(self, given_bank):
        self.row_index += 1
        self.withdraw_label = Label(self.root, text="Withdraw:  Account Number:").grid(row=self.row_index,
                                                                                       column=1)
        self.withdraw_account_entry = Entry(self.root, textvar=self.withdraw_account_entry)
        self.withdraw_account_entry.grid(row=self.row_index, column=2)
        self.withdraw_amount_label = Label(self.root, text="Amount: ").grid(row=self.row_index, column=3)
        self.withdraw_amount_entry = Entry(self.root, textvar=self.withdraw_amount_entry)
        self.withdraw_amount_entry.grid(row=self.row_index, column=4)
        self.withdraw_button = Button(self.root, text="Commit Withdraw",
                                      command=lambda: self.commit_withdraw(given_bank)).grid(
            row=self.row_index, column=7)

    def handle_status_label(self):
        self.row_index += 1
        self.status_label = Label(self.root, text="Status:").grid(row=self.row_index, column=1)
        self.updated_status_label = Label(self.root, text="Probably The Greatest Bank In The Universe....")
        self.updated_status_label.grid(row=self.row_index, column=2)

    def commit_transaction(self, given_bank):
        amount_to_transact = int(self.transaction_amount_entry.get())
        account_from = given_bank.get_account_from_a_given_account_number(self.transaction_account_from_entry.get())
        account_to = given_bank.get_account_from_a_given_account_number(self.transaction_account_to_entry.get())
        if account_from is -1:
            self.updated_status_label.config(text="Account From's Number Wasn't Found!!")
            return
        if account_to is -1:
            self.updated_status_label.config(text="Account To's Number Wasn't Found!!")
            return
        else:
            transaction_status = account_from.transact_amount_to(account_to, amount_to_transact)
            if transaction_status is -1:
                self.updated_status_label.config(text="The Account From's Credit Frame Is Not High Enough ")
                print("Invalid Operation!! The Account From's Credit Frame Is Not High Enough,",
                      "Transaction Wasn't Committed And Wasn't Recorded In Logger File")
            else:
                self.update_gui(given_bank)
                self.updated_status_label['text'] = 'The Transaction Was Committed Successfully!!!'
                print('{} passed {} Shekels to {}'.format(account_from.name, amount_to_transact, account_to.name))
                logger.info('{} passed {} Shekels to {}'.format(account_from.name, amount_to_transact, account_to.name))

    def commit_deposit(self, given_bank):
        amount_to_deposit = self.deposit_amount_entry.get()
        account_to = given_bank.get_account_from_a_given_account_number(self.deposit_account_entry.get())
        if account_to is -1:
            self.updated_status_label.config(text="Deposit: Account's Number Wasn't Found!!")
        else:
            account_to.deposit(amount_to_deposit)
            self.update_gui(given_bank)
            self.updated_status_label['text'] = 'The Deposit Was Committed Successfully!!!'

    def commit_withdraw(self, given_bank):
        amount_to_withdraw = self.withdraw_amount_entry.get()
        account_to = given_bank.get_account_from_a_given_account_number(self.withdraw_account_entry.get())
        if account_to is -1:
            self.updated_status_label.config(text="Withdraw: Account's Number Wasn't Found!!!")
        else:
            withdraw_status = account_to.withdraw(amount_to_withdraw)
            if withdraw_status is -1:
                self.updated_status_label.config(text="Invalid Operation! You've Reached The Credit Frame Limit!!")
            else:
                self.update_gui(given_bank)
                self.updated_status_label['text'] = 'The Withdraw Was Committed Successfully!!!'

    def handle_words_timer(self, words_timer):
        self.row_index += 1
        self.get_words_button = Button(self.root, text="Get Words", command=lambda: words_timer.start_words()).grid(
            row=self.row_index, column=1)
        self.stop_button = Button(self.root, text="Stop Getting Words", command=lambda: words_timer.stop_words()).grid(
            row=self.row_index, column=2)
        self.reset_button = Button(self.root, text="Reset", command=lambda: words_timer.reset()).grid(
            row=self.row_index, column=3)
        self.radio_button_include = Radiobutton(self.root, text="Include", variable=self.radio_var,
                                                value=True).grid(
            row=self.row_index, column=4)
        self.radio_button_exclude = Radiobutton(self.root, text="Exclude", variable=self.radio_var,
                                                value=False).grid(
            row=self.row_index, column=5)
        self.char_label = Label(self.root, text="Enter Char:").grid(row=self.row_index, column=6)
        self.char_entry = Entry(self.root, textvar=self.entry_var)
        self.char_entry.grid(row=self.row_index, column=7)
        self.words_timer_status_label = Label(self.root, text="Probably The Greatest Words_Timer In The Universe....")
        self.words_timer_status_label.grid(row=self.row_index + 1, column=2)


class WordsTimer:
    def __init__(self, the_root, row_index_to_start):
        self.root = the_root
        self.file = open('word.txt', 'r')
        self.graph_file = None  # in case there was another file for the graph
        self.row = row_index_to_start
        self.row = self.row + 1
        # self.root.row_index += 1
        self.get_words_button = Button(self.root, text="Get Words", command=self.start_words).grid(
            row=self.row, column=1)
        self.button_stop = Button(self.root, text="Stop Getting Words", command=self.stop_words).grid(
            row=self.row, column=2)
        self.reset_button = Button(self.root, text="Reset", command=self.reset).grid(
            row=self.row, column=3)
        self.radio_var = BooleanVar()
        self.entry_var = StringVar()
        self.radio_button_include = Radiobutton(self.root, text="Include", variable=self.radio_var, value=True).grid(
            row=self.row, column=4)
        self.radio_button_exclude = Radiobutton(the_root, text="Exclude", variable=self.radio_var, value=False).grid(
            row=self.row, column=5)
        self.label_char = Label(the_root, text="Enter Char:").grid(
            row=self.row, column=6)
        self.entry_char = Entry(the_root, textvar=self.entry_var).grid(
            row=self.row, column=7)
        self.gets_words_bool = False
        self.x = self.words_generator(self.entry_var.get(), self.radio_var.get())

    def words_generator(self, the_char, boolean):
        print("we call generator the char is: " + the_char + " the bool is: " + str(boolean))

        for each_line in self.file:
            words_list = re.split("[, \ .]", each_line)
            for each_word in words_list:
                if boolean is True:
                    if each_word.lower().__contains__(the_char.lower()):
                        logger.info(each_word)
                        yield each_word
                else:
                    if not each_word.lower().__contains__(the_char.lower()):
                        logger.info(each_word)
                        yield each_word

    def get_word(self):
        if self.gets_words_bool is True:
            for each_word in self.x:
                print(each_word)
                self.root.after(2000, self.get_word)
                return each_word

    def stop_words(self):
        print("stop")
        logger.info("stop")
        self.gets_words_bool = False

    def reset(self):
        print("reset called")
        logger.info("reset called")
        self.file = open('word.txt', 'r')
        self.gets_words_bool = True
        self.x = self.words_generator(self.entry_var.get(), self.radio_var.get())
        self.get_word()

    def start_words(self):
        self.gets_words_bool = True
        self.x = self.words_generator(self.entry_var.get(), self.radio_var.get())
        self.get_word()

    # def make_a_graph(self):
    # dictionary_chars_appearance = {}
    # self.graph_file = open('word.txt', 'r')
    # with self.graph_file as f:
    #  for line in f:
    #       words_list = re.split("[, \ .]", line)
    #        print("The Line: " + line)
    #         for word in words_list:
    #              word = word.upper()
    #               for char in word:
    #                    if not char in dictionary_chars_appearance:


#                         dictionary_chars_appearance[char] = 1
#                      else:
#                           dictionary_chars_appearance[char] += 1
#
#           # print(word)
#        print('-------------------------')

# print(dictionary_chars_appearance)
#  items = list(dictionary_chars_appearance.keys())
#   values = list(dictionary_chars_appearance.values())
#    plt.bar(items[0:10], values[0:10])
#     plt.xlabel('Chars')
#      plt.ylabel('Appearance Number')
#       plt.title('Chars Appearance')
#        plt.show()


the_bank = TheBank()
hamami_account = Account("Hamami", 1, 3000, 1500)
ariel_account = Account("Ariel", 2, 2000)
omer_account = Account("Omer", 3, 1000, 1500)

the_bank.add_account_to_account_list(hamami_account)
the_bank.add_account_to_account_list(ariel_account)
the_bank.add_account_to_account_list(omer_account)

for account_balance in the_bank.get_accounts_balance():
    print('Balance is: ', account_balance)

root = Tk()
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)
bankGui = TkGui(topFrame)
bankGui.update_gui(the_bank)
print('the row we enter is: {}'.format(bankGui.row_index))
app = WordsTimer(bottomFrame, bankGui.row_index)
# app.make_a_graph()
root.mainloop()
