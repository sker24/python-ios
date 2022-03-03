# REQUIREMENTS
# Script needs to Configure EIGRP on a network device within the topology and advertise networks appropriately

# SOURCES
# https://www.paramiko.org/

# import the necessary libraries
import paramiko
import time

# device information, we could also ask the user to input this information
destination = "8.0.0.1"
user = "admin"
passwd = "cisco"

# initiate the SSH connection
ssh_client = paramiko.SSHClient()

# Use a Trust All policy
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Initiate connection with specified variables
ssh_client.connect(hostname=destination, username=user, password=passwd)
ssh = ssh_client.invoke_shell()

# commands to prove the script worked
ssh.send("enable\n")
ssh.send("cisco\n")
ssh.send("conf t\n")
# enable the EIGRP routing protocol with an ASN of 10
ssh.send("router eigrp 10\n")
# set the router-id
ssh.send("eigrp router-id 1.1.1.1\n")
# advertise a connected network
ssh.send("network 8.0.0.0\n")
ssh.send("end\n")
ssh.send("exit\n")

# receive the output and print it
time.sleep(1)
output = ssh.recv(65535)
print(output)