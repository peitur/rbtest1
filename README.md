# rbtest1

Worst possible web app ... designewise and securitywise

Run this on dedicated VM.

## Install

RHEL/CentOS
```
yum install python3.6
pip install -r requirements.txt
```

In virtualenv
```
cd code
virtualenv .
source bin/activate
pip install -r requirements.txt
```

## init

```
cd code
python3 init.py
```

## use

```
cd code
python3 server.py
```
