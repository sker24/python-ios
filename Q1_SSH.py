# REQUIREMENTS
# Script needs to connect to a layer 3 device with a secure protocol

# SOURCES
# https://www.paramiko.org/

# import the necessary libraries
import paramiko
import time

# hardcoded device information, we could also ask the user to input this information
destination = "223.0.1.2"
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
ssh.send("int lo1\n")
ssh.send("ip add 99.99.99.99 255.255.255.255\n")
ssh.send("desc SSH WORKS!\n")
ssh.send("end\n")
ssh.send("exit\n")

# receive the output and print it
time.sleep(1)
output = ssh.recv(65535)
print(output)