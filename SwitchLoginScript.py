#!/usr/bin/env python

import getpass
import sys
import telnetlib

user = input("Enter your telnet username: ")
password = getpass.getpass()


for n in range(1, 4):
    print("Telnet to host" + str(n))
    HOST = "223.0.2." + str(n)
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(user.encode('utf-8') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('utf-8') + b"\n")
    tn.write(b"enable\n")
    tn.write(b"cisco\n")
    tn.write(b"conf t\n")

    for n in range(2, 21):
        tn.write(b"vlan " + str(n).encode('utf-8') + b"\n")
        tn.write(b"name Python_VLAN_" + str(n).encode('utf-8') + b"\n")

    tn.write(b"end\n")
    tn.write(b"exit\n")

    print(tn.read_all())


