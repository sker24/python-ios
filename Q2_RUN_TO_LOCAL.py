# REQUIREMENTS
# Script to compare the running-configuration to a local offline configuration
# Script to compare the running-configuration to the startup configuration

# SOURCES
# we can use this library -> https://docs.python.org/3/library/telnetlib.html
# and this one ------------> https://docs.python.org/2/library/difflib.html
# and this one too --------> https://docs.python.org/3/library/ipaddress.html


# import necessary libraries
import difflib
import telnetlib
import ipaddress

# function that accepts only valid IP addresses as input
def ipentered():
    while True:
        try:
            val = input("Enter the target device ip address: ")
            # using the ipaddress module to accept input only in an ip format
            return ipaddress.ip_address(val)
        except ValueError:
            print("Not a valid IP address")


# call the function
targetip = ipentered()


# function that get either the running or startup configurations
def getconf(targetip, runorstart, filename):
    # device authentication credentials
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
    # if the parameter is run, get the running config
    if runorstart == "run":
        tn.write(b"show run\n")
        tn.write(b"exit\n")
    # if the parameter is start, get the startup config
    elif runorstart == "start":
        tn.write(b"show start\n")
        tn.write(b"exit\n")

    # save output into a file
    conf = tn.read_all()
    confb = open(filename, "w")
    confb.write(conf.decode('utf-8'))
    confb.write("\n")
    confb.close()
    return


# function that starts a menu to choose the type of comparison
def print_menu():
    print("")
    print("Choose type of comparison")
    print("_________________________")
    print("1. Startup-Configuration ")
    print("2. Local File")
    print("3. Exit")
    choice = 0
    # utilising a while loop and also handling value errors
    while 1 > choice or 4 < choice:
        try:
            choice = int(input("[1-3]: "))
        except ValueError:
            print("Try again: ")
    # if choice is 1, use the show archive config diff command and save the output
    if choice == 1:
        print("Comparing " + str(targetip), "'s running and startup configurations")
        # run the show archive config diff command
        user = "admin"
        password = "cisco"
        tn = telnetlib.Telnet(str(targetip))
        tn.read_until(b"Username: ")
        tn.write(user.encode('utf-8') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('utf-8') + b"\n")
        tn.write(b"enable\n")
        tn.write(b"cisco\n")
        tn.write(b"show archive config diff\n")
        # printing command output, from telnetlib documentation
        print(tn.read_eager())
        tn.write(b"exit\n")

        # save the output into a file
        out = tn.read_all()
        conf = open("Conf_result", "w")
        conf.write(out.decode('utf-8'))
        conf.write("\n")
        conf.close()

        filetp = open("Conf_result", "r")
        print(filetp.read())

    # if choice is 2, we use the difflib library to compare the two configurations
    elif choice == 2:
        while True:
            try:
                # asking the user for a local filename to compare the running configuration with
                fname = input("Enter a local filename: ")
                lfile = open(fname, 'r')
                run = open("run_conf", 'r')
                # https://stackoverflow.com/questions/15864641/python-difflib-comparing-files
                # using the difflib to compare the files and parsing the output
                diff = difflib.ndiff(lfile.readlines(), run.readlines())
                delta = ''.join(x[2:] for x in diff if x.startswith('- '))
                print("")
                # will print differences found in the local file only
                print("Additional/Different commands found in  --> " + fname)
                print("_______________________________________")
                print("")
                print(delta)
            # error handling
            except FileNotFoundError:
                print("File Not found!")

    else:
        print()


# calling the functions
getconf(targetip, "run", "run_conf")
print_menu()

