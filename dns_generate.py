#!/usr/bin/python36

##############
# HEADER
# Author:   Melvin Suter
# Version:  1.0
# Git-Repo: https://github.com/melvin-suter/dns_generator
# Purpose:
#   Generates a .zone file out of readable .yaml files
#   Can load universal usable modules into domains
##############

##############
# IMPORTS
##############
import os
import yaml
import datetime  
import glob


##############
# CONFIG
##############
CONFIG_DATA='/opt/dns_generator/data'
CONFIG_MODULES='/opt/dns_generator/modules'
CONFIG_OUTPUT='/var/named/zones'


##############
# FUNCTIONS
##############
def getSerial():
    now=datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M")

##############
# SCRIPT
##############

# Clear output
import glob, os, os.path

filelist = glob.glob(os.path.join(CONFIG_OUTPUT, "*.zone"))
for f in filelist:
    os.remove(f)

# Creating Zone-List String
listString = ""

# Loop Thorugh files in data/*.yaml
for file in os.listdir(CONFIG_DATA):
    if file.endswith(".yaml"):
        # Read file
        with open(CONFIG_DATA+'/'+file, 'r') as stream:
            try:
                # Load Yaml
                data=(yaml.safe_load(stream))

                # Creating Zone String
                zoneString = "$TTL " + str(data['globalttl']) + "\n"

                zoneString = zoneString + "@       IN      SOA     " + data['domainname'] + ". dnsmaster (\n"
                zoneString = zoneString + "                " + getSerial() + "    ;Serial\n"
                zoneString = zoneString + "                " + str(data['soa']['refresh']) + "            ;Refresh\n"
                zoneString = zoneString + "                " + str(data['soa']['retry']) + "            ;Retry\n"
                zoneString = zoneString + "                " + str(data['soa']['expire']) + "           ;Expire\n"
                zoneString = zoneString + "                " + str(data['soa']['minimum']) + "             ;Minimum\n"
                zoneString = zoneString + ")\n"

                # Loop through selected modules
                for module in data['modules']:
                    try:
                        # Try to read module
                        with open(CONFIG_MODULES+'/' + module.lower() + '.yaml', 'r') as innerStream:
                            innerdata=(yaml.safe_load(innerStream))
                            zoneString = zoneString + "\n\n;Module " + innerdata['name'] + "\n"
                            for record in innerdata['records']:
                                zoneString = zoneString + ("{name:20} IN {type:5} {value}\n".format(**record)).replace('{DOMAINNAME}',data['domainname'])
                    except:
                        print("")
                    
                if(data['records'] is not None):
                    zoneString = zoneString + "\n\n;Records\n"
                    for record in data['records']:
                        zoneString = zoneString + "{name:20} IN {type:5} {value}\n".format(**record)

                outputPath = CONFIG_OUTPUT+'/'+file[:-4]+'zone'
                with open(outputPath, 'w') as innerstream:
                    innerstream.write(zoneString)

                listString = listString + "zone \"" + data['domainname'] + "\" IN {\n"
                listString = listString + "        type master;\n"
                listString = listString + "        file \"" + outputPath + "\";\n"
                listString = listString + "        allow-update { none; };\n"
                listString = listString + "};\n"


            except yaml.YAMLError as exc:
                print(exc)

with open(CONFIG_OUTPUT+'/_global.zone', 'w') as stream:
    stream.write(listString)