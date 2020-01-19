# pc_control_local
### Control your PC from mobile device in local network

##### Requierments:
- python 3
- pip
- flask
- pyautogui
- hammer (JS library)

## Installation steps:
- Clone repo
- Install requirments
- Add chrome to PATH
- Download some contrast cursor, name it cur.cur and place it to project folder (pc_control_local)
- Download hammer.min.js into js folder (possible url: https://hammerjs.github.io/dist/hammer.min.js)
- Bind your computer MAC address to IP in router settings, and create ip.txt file containing binded ip in project folder

Firs steps could be done by typing next commands in command line window (type 'cmd' in windows start menu):

```
D:
git clone https://github.com/xzxzxc/pc_control_local
cd pc_control_local
pip install -r requirements.txt
setx path "%path%;C:\Program Files (x86)\Google\Chrome\Application"
```
> Supports windows only for now

> To add programm to autostart - create icon of local_server.bat and place it to "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup" folder

> Host name must ocntains only latin symbols - flask wsgsi limitation (((

## For developers:
>  Note that templates\buttons_base.html mus be encoded as UTF-8 without BOM, otherwise <!doctype> would be ignored

### TODO tasks:
- add typing ability
- log fron errors in log.txt
- add ability to open custom url in browser
- add ability to setup chrome users count
