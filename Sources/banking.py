# Simple Banking System

import random
import sqlite3


# the_list = dict()


def generate_checksum(card):
    list_number = list(card)
    for i in range(len(list_number)):
        list_number[i] = int(list_number[i])
        if i % 2 == 0:
            list_number[i] *= 2
    for i in range(len(list_number)):
        if list_number[i] > 9:
            list_number[i] -= 9
    sum = 0
    for num in list_number:
        sum += num
    checksum = (10 - (sum % 10)) % 10
    return card + str(checksum)


def save_card(card, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO card (id, number, pin, balance)
    VALUES (?,?,?,?)''', (1, card, pin, 0))
    # cur.execute('SELECT * FROM card WHERE number=?', (card,))
    # print(cur.fetchone())
    conn.commit()


def card_exists(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT count(*) FROM card WHERE number=?', (card,))
    conn.commit()
    if cur.fetchone() == (1,):
        return True
    else:
        return False


def create_account():
    print("Your card has been created")
    print("Your card number:")
    while True:
        new_card = "400000" + str("%.9d" % (random.randint(0, 999999999)))
        new_card = generate_checksum(new_card)
        if not card_exists(new_card):
            break
    print(new_card)
    new_pin = str("%.4d" % (random.randint(0, 9999)))
    print("Your card PIN")
    print(new_pin)
    save_card(new_card, new_pin)
    # the_list[new_card] = new_pin


def balance(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number=?', (card,))
    balance = cur.fetchone()[0]
    conn.commit()
    print("Balance: %s" % balance)


def add_income(card):
    print("Enter income:")
    income = int(input())
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number=?', (card,))
    balance = cur.fetchone()[0]
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (balance + income, card))
    conn.commit()
    print("Income was added")


def validate_card(card):
    list_number = list(card)
    orig_checksum = list_number.pop()
    for i in range(len(list_number)):
        list_number[i] = int(list_number[i])
        if i % 2 == 0:
            list_number[i] *= 2
    for i in range(len(list_number)):
        if list_number[i] > 9:
            list_number[i] -= 9
    sum = 0
    for num in list_number:
        sum += num
    checksum = (10 - (sum % 10)) % 10
    return checksum == int(orig_checksum)


def check_amount(card, amount):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number=?', (card,))
    balance = cur.fetchone()[0]
    if balance >= amount:
        return True
    else:
        return False


def actual_transfer(card, dest, amount):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute('SELECT balance FROM card WHERE number=?', (card,))
    balance = cur.fetchone()[0]
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (balance - amount, card))

    cur.execute('SELECT balance FROM card WHERE number=?', (dest,))
    balance = cur.fetchone()[0]
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (balance + amount, dest))

    conn.commit()
    print("Success!")


def do_transfer(card):
    print("Transfer")
    print("Enter card number:")
    dest = input()
    if validate_card(dest):
        if card_exists(dest):
            print("Enter how much money you want to transfer:")
            amount = int(input())
            if check_amount(card, amount):
                actual_transfer(card, dest, amount)
            else:
                print("Not enough money!")
        else:
            print("Such a card does not exist.")
    else:
        print("Probably you made a mistake in the card number. Please try again!")


def close_account(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('DELETE FROM card WHERE number=?', (card,))
    conn.commit()
    print("The account has been closed!")


def logged_menu(card):
    while True:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = input()
        if choice == "0":
            print("Bye")
            return False
        elif choice == "1":
            balance(card)
        elif choice == "2":
            add_income(card)
        elif choice == "3":
            do_transfer(card)
        elif choice == "4":
            close_account(card)
            return True
        elif choice == "5":
            print("You have successfully logged out!")
            return True
        else:
            print("Unexpected")
            return False


def card_check(card, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('''SELECT count(*)
    FROM card
    WHERE number = (?)
    AND pin = (?)''', (card, pin))
    conn.commit()
    if cur.fetchone() == (1,):
        return True
    else:
        return False


def login():
    print("Enter your card number:")
    card = input()
    print("Enter your PIN:")
    pin = input()
    # if card in the_list and the_list[card] == pin:
    if card_check(card, pin):
        print("You have successfully logged in!")
        return logged_menu(card)
    else:
        print("Wrong card number or PIN")
        return True


def main_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")
    choice = input()
    if choice == "0":
        return False
    elif choice == "1":
        create_account()
        return True
    elif choice == "2":
        return login()
    else:
        print("Unexpected")


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE if not exists card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER default 0
    );""")
conn.commit()

while main_menu():
    pass
