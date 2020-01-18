set /p IP=<ip.txt
set FLASK_APP=local_server.py
flask run --host=%IP%
