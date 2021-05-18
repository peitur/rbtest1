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

## simplesum.sh

Decode nonsalted hashed passwords
```
cd code
simplesum.sh ../examples/10k-worst-passwords.txt users.txt md5
```

File format for users:
```
username:hashedpassword
```

Example:
```
user1:wkjnefkwjenfkwjenfkwjefnkweuwi37rh24ir72348fhewi
user2:9283fn2938fn293fn2983fnwiendfw98j9jofhwnow3fg8w3
``
