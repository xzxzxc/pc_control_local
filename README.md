# pc_control_local
Control your PC from mobile device in local network

Supports windows only for now
Host must ocntains only latin symbols - flask wsgsi limitation (((
Chrome need to be added to PATH (setx path "%path%;C:\Program Files (x86)\Google\Chrome\Application")

Requierments:
python 3
pip
flask
pyautogui
hammer (JS library)

Installation steps:
Create project directory and go there: mkdir pc_control_local && cd pc_control_local
Clone repo: git clone https://github.com/xzxzxc/pc_control_local
Install requirments: pip install -r requirements.txt
Download some contrast cursor, name it cur.cur and place it to project folder
Download hammer.min.js into js folder (possible url: https://hammerjs.github.io/dist/hammer.min.js)
Bind your computer MAC address to IP in router settings, and create ip.txt file containing binded ip in project folder

To add to autostart - create icon and place it to "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup" folder

For developers: note that templates\buttons_base.html mus be encoded as UTF-8 without BOM, otherwise <!doctype> would be ignored
TODO tasks:
create dispatcher.js
log fron errors in log.txt
add typing ability
add ability to open custom url in browser
add ability to setup chrome users count
