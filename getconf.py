import telnetlib

targetip = input("ip: ")


def getconf(targetip, runorstart, filename):
    user = "admin"
    password = "cisco"
    t = telnetlib.Telnet(targetip)
    t.read_until(b"Username: ")
    t.write(user.encode('utf-8') + b"\n")
    if password:
        t.read_until(b"Password: ")
        t.write(password.encode('utf-8') + b"\n")
    t.write(b"enable\n")
    t.write(b"cisco\n")
    t.write(b"terminal length 0\n")
    if runorstart == "run":
        t.write(b"show run\n")
        t.write(b"exit\n")
    elif runorstart == "start":
        t.write(b"show start\n")
        t.write(b"exit\n")

    conf = t.read_all()
    confb = open(filename, "w")
    confb.write(conf.decode('utf-8'))
    confb.write("\n")
    confb.close()
    return


getconf(targetip, "run", "test2")