import winreg

SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
user32Dll = None
try:
	from ctypes import WinDLL
	user32Dll = WinDLL('user32')
except:
	pass


allowed_keys=['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']


REG_PATH = r"Control Panel\Cursors"

def set_reg(name, value, reg_path=None):
	try:
		winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path or REG_PATH, 0, winreg.KEY_WRITE)
		winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
		winreg.CloseKey(registry_key)
		return True
	except WindowsError as e:
		print(str(e))
		return False

def get_reg(name, reg_path=None):
	try:
		registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path or REG_PATH, 0, winreg.KEY_READ)
		value, regtype = winreg.QueryValueEx(registry_key, name)
		winreg.CloseKey(registry_key)
		return value
	except WindowsError as e:
		print(str(e))
		return None

enable_hex_reg = 'Control Panel\Input Method'
enable_hex_reg_key = 'EnableHexNumpad'
enable_hex_reg_val = get_reg(enable_hex_reg_key, enable_hex_reg)
if enable_hex_reg_val is None or enable_hex_reg_val != '1':
	set_reg(enable_hex_reg_key, '1', enable_hex_reg)

def chunks(lst, n):
	for i in range(0, len(lst), n):
		yield lst[i:i + n]


def update_cur():
	if user32Dll is not None:
		user32Dll.SystemParametersInfoW(SPI_SETCURSORS,0,0,SPIF_UPDATEINIFILE|SPIF_SENDCHANGE)
