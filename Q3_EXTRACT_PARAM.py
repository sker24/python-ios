# REQUIREMENTS
# Script needs to collect the routing table, vlan database, IOS version and CPU performance stats
# Script needs to export all of the above parameters in a MySQL database
# Script needs to be set to run at time intervals

# SOURCES
# we can use this library -> https://docs.python.org/3/library/telnetlib.html
# and this one too --------> https://docs.python.org/3/library/ipaddress.html
# and this one ------------> https://docs.python.org/3/library/sqlite3.html

# import necessary libraries
import telnetlib
import ipaddress
import sqlite3


# function that accepts only valid IP addresses as input
def ipentered():
    while True:
        try:
            val = input("Enter the target device ip address: ")
            # using the ipaddress module to accept input only in an ip format
            return ipaddress.ip_address(val)
        except ValueError:
            print("Not a valid IP address")


# getting all necessary input from user
targetip = ipentered()
user = input("Enter your account username: ")
password = input("Enter your password: ")


# function that runs a single command from the exec mode and saves the output into a file
def runcmd(targetip, cmd, filename):
    # filename naming convention
    filename = (str(targetip) + "_" + filename)
    user = "admin"
    password = "cisco"
    # initiate the telnet connection
    tn = telnetlib.Telnet(str(targetip))
    # read until we get prompted for a username and pass and input the credentials
    tn.read_until(b"Username: ")
    tn.write(user.encode('utf-8') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('utf-8') + b"\n")
    # commands that place the user into privilege exec mode
    tn.write(b"enable\n")
    tn.write(b"cisco\n")
    tn.write(b"terminal length 0\n")
    # this is where the command we entered as a parameter is used
    tn.write(b"" + cmd + b"\n")
    tn.write(b"exit\n")

    # save output into a file
    conf = tn.read_all()
    confb = open(filename, "w")
    confb.write(conf.decode('utf-8'))
    confb.write("\n")
    confb.close()
    return


# Here im calling the function runcmd to get all of the necessary information
# This is not a very efficient way, because we are initiating a new connection
# every time we call the function, we could improve this by making a single connection for
# all the files we need instead

print("Getting the routing table")
runcmd(targetip, b"show ip route", "routing-table")

print("Getting the vlan database")
runcmd(targetip, b"show vlan brief", "vlan-database")

print("Getting the ios version")
runcmd(targetip, b"show version", "ios-version")

print("Getting the cpu-performance")
runcmd(targetip, b"show proc cpu history", "cpu-performance")

print("All parameters successfully saved!")


# variables that are assigned to the files with device parameters
routing = open(str(targetip) + "_" + "routing-table", "r")
vlan = open(str(targetip) + "_" + "vlan-database", "r")
ios = open(str(targetip) + "_" + "ios-version", "r")
cpu = open(str(targetip) + "_" + "cpu-performance", "r")

# variables that read the text from the files
routingf = routing.readline()
vlanf = vlan.readline()
iosf = ios.readline()
cpuf = cpu.readline()

# creating a database called example.db
con = sqlite3.connect('example.db')
# creating a cursor object to then call the execute method to perform SQL commands
c = con.cursor()

# in this function we create a table called info, and create four text columns
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS info(routing TEXT, vlan TEXT, ios TEXT, cpu TEXT)")

# This is where I couldn't get it to work, I have the files with the parameters
# to enter the database as variables, but the database ends up being empty
def data_entry():
    c.execute("INSERT INTO info(routing, vlan, ios, cpu) VALUES (?, ?, ?, ?)",
              (routingf, vlanf, iosf, cpuf))
    # save changes to the database
    con.commit()
    # close the database to prevent unnecessary memory usage
    c.close()
    con.close()


# call above functions
create_table()
data_entry()

