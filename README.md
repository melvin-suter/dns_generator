# Installation

```
yum install -y python36-pip python36
pip install toml
```

Add this line to the end of /etc/named.conf
```
include "/var/named/zones/_globa.zone";
```

Add .yaml modules according to the example_webserver.yaml:
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

Add .yaml files according to the example.com.yaml:
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