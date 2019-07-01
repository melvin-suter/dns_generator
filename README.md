# Installation

## Dependencies
```
yum install -y epel-release
yum install -y python36-pip python36
pip3.6 install pyyaml
```

## Git repo
```
mkdir /opt/dns_generator/
cd /opt/dns_generator/
git clone https://github.com/melvin-suter/dns_generator.git .
```

## Config

Add this line to the end of /etc/named.conf
```
include "/var/named/zones/_global.zone";
```

Add .yaml modules according to the `example_webserver.yaml` in the direcotry `/opt/dns_generator/modules`:
```
name : "Example Webserver"
records :
- name : "@"
  type : "A"
  value : "1.2.3.4"
- name : "*"
  type : "CNAME"
  value : "{DOMAINNAME}."
```

Add .yaml files according to the `example.com.yaml`in the directory `/opt/dns_generator/data`:
```
domainname : "example.com"
globalttl : 3600
soa :
  refresh : 3600
  retry : 3600
  expire : 86400
  minimum : 300
modules :
- example_webserver
- example_ns
records :
- name : "sub"
  type : "A"
  value : "4.3.2.1"
```

Run the `/opt/dns_generator/dns_generate.py` file.
