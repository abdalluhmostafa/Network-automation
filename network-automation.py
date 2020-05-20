#!/usr/bin/python
# Automation Task
# This code get { Hostname, Model, Uptime, software version, serial, Mac } from Cisco routers using netmiko library and GNS3
# This code by Abdalluh Mostafa
# abdalluh.mostafa@gmail.com

from netmiko import ConnectHandler
import re
import json

cisco = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.15', # ssh IP
        'username': 'admin',  # ssh username
        'password': 'password',  # ssh password
    }

net_connect = ConnectHandler(**cisco)

output = net_connect.send_command('show version')  # execute show version on router and save output to output object

# finding hostname in output using regular expressions
regex_hostname = re.compile(r'(\S+)\suptime')
hostname = regex_hostname.findall(output)

# finding model in output using regular expressions
regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
model = regex_model.findall(output)

# finding uptime in output using regular expressions
regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
uptime = regex_uptime.findall(output)

# finding version in output using regular expressions
regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
version = regex_version.findall(output)

# finding serial in output using regular expressions
regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
serial = regex_serial.findall(output)

output_mac = net_connect.send_command('sh ip arp | include - ') # execute sh ip arp | include -  on router and save output to output_mac object

# finding Active MACs in output_mac using regular expressions
regex_model = re.compile(r'\-  \s(\S+)')
mac = regex_model.findall(output_mac)

# Print In JSON format
print ("\nJSON Format\n")
#devices = [([hostname[0],model[0],uptime[0],version[0],serial[0],mac[0:]])] # Format without define
devices = [(['hostname: {}'.format(hostname[0]),'model: {}'.format(model[0]),'uptime: {}'.format(uptime[0]),'version: {}'.format(version[0]),'serial: {}'.format(serial[0]),'mac: {}' .format(mac[0:])])]
info =  json.dumps(devices) # FOR JSON FORMAT
print  info
