import socket
import sqlite3

conn = sqlite3.connect("tcpDB.db")
c = conn.cursor()
print("connect success")

# c.execute('''CREATE TABLE user
#        (
#         ID INTEGER PRIMARY KEY   AUTOINCREMENT,
#        name           TEXT    NOT NULL,
#        password       TEXT    NOT NULL)
#        ;''')

HOST = '0.0.0.0'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def hello(self):
        print(f"Hello {self.name}")


cursor = conn.execute("SELECT name,password FROM user ")

while True:
    print("switch mode")
    print("1.login , 2.register")
    chose = int(input())
    if chose == 1:
        print("enter your name and password")
        user = User(input(), input())

        flag = False
        for item in cursor:
            name = item[0]
            password = item[1]
            if user.name == name and user.password == password:
                flag = True

        if flag:
            user.hello()
            while True:
                outdata = input(' input message: ')
                print('send: ' + outdata)
                s.send(outdata.encode())
                indata = s.recv(1024)
                if len(indata) == 0:  # connection closed
                    s.close()
                    print('server closed connection.')
                    break
                print('recv: ' + indata.decode())
        else:
            print("error")
            print("==============================")
    elif chose == 2:
        print("enter your name")
        uname = input()
        print("enter your password")
        upassword = input()
        param = (uname,upassword)
        c.execute("INSERT INTO user VALUES (NULL,?,?)",param)
        conn.commit()
        print("success insert")
        print("==============================")
        conn.close()
    else:
        print("have wrong")
