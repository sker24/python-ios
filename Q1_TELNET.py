# REQUIREMENTS
# Script needs to use telnet to connect to a network device
# Script needs to backup configuration from multiple switches

# SOURCES
# we can use this library -> https://docs.python.org/3/library/telnetlib.html

# import the necessary libraries
import telnetlib

# ask the user for the account name and call the getpass library to get the password
user = input("Enter your account username: ")
password = input("Enter your password: ")

# utilising a for loop for the target IP addresses
for n in range(1, 4):
    HOST = "223.0.2." + str(n)
    # prints a message for every IP it goes through
    print("Fetching " + HOST + "\'s running-configuration")
    # calling the telnetlib library to initiate the connection
    t = telnetlib.Telnet(HOST)
    # reading until we get prompted for a username and password and input the requested credentials
    t.read_until(b"Username: ")
    t.write(user.encode('utf-8') + b"\n")
    if password:
        t.read_until(b"Password: ")
        t.write(password.encode('utf-8') + b"\n")
    # get the running configuration
    t.write(b"enable\n")
    t.write(b"cisco\n")
    t.write(b"terminal length 0\n")
    t.write(b"show run\n")
    t.write(b"exit\n")

    # save the configurations in separate files with write permission
    conf = t.read_all()
    confb = open("Switch-IP-" + HOST, "w")
    confb.write(conf.decode('utf-8'))
    confb.write("\n")
    confb.close()


