#!/bin/bash

cp -f nginx-badsite.conf /etc/nginx/conf.d/badsite.conf
cp -f systemd-badsite.service /usr/lib/systemd/system/badsite.service
cp -f uwsgi-badsite.ini $(pwd)/../badsite.ini

systemctl daemon-reload

systemctl stop badsite
systemctl start badsite

systemctl stop nginx
systemctl start nginx
