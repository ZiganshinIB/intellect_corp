#!/bin/bash
set -e
git pull
/opt/intellect_corp/.venv/bin/pip install -r requirements.txt
/opt/intellect_corp/.venv/bin/python /opt/intellect_corp/i_corp/manage.py migrate
systemctl restart redis.service
systemctl disable icorp.service
systemctl restart icorp.service
systemctl enable icorp.service