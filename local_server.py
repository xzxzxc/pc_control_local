# coding=utf-8
try:
	from flask import Flask, redirect, url_for, render_template, request, send_from_directory, send_file, jsonify, redirect
	import os, datetime, pyautogui, sys, string, logging, time, socket, subprocess, re, threading, pyperclip, pyscreeze, hashlib, io, base64
	from misc import user32Dll, allowed_keys, set_reg, get_reg, chunks, update_cur
	from win32api import GetSystemMetrics
	from PIL import Image
	from typing import Dict, Tuple, Sequence
except:
	subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
	print(subprocess.run(['.\local_server.bat'], shell=True))
	exit()

DEBUG = __name__ == '__main__'
log_level = logging.DEBUG if DEBUG else logging.ERROR

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(log_level)
if not DEBUG:
	logging.basicConfig(filename='log.txt')

pyautogui.FAILSAFE = False

flag_names = ['Arrow', 'Help', 'AppStarting', 'Wait', 'Crosshair', 'IBeam', 'NWPen', 'No', 'SizeNS', 'SizeWE', 'SizeNWSE', 'SizeNESW', 'SizeAll', 'UpArrow', 'Hand']
new_flag_val = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cur.cur')
norm_values = {x: get_reg(x) for x in flag_names}

def move_internal(deltaX, deltaY, duration):
	deltaX, deltaY, duration = float(deltaX), float(deltaY), float(duration or '0.1')
	for flag_name in flag_names:
		set_reg(flag_name, new_flag_val)
	update_cur()
	pyautogui.moveRel(deltaX, deltaY, duration=duration)
	for flag_name in flag_names:
		set_reg(flag_name, norm_values[flag_name])
	threading.Timer(0.8, update_cur).start()

def press_internal(keys, repeats):
	key_sets = keys.split(';')
	for _ in range(min(int(repeats or 1), 25)):
		for k_set in key_sets:
			pyautogui.hotkey(*k_set.split('+'))
			time.sleep(.01)

hextypeKey = 'altleft' if os.name == 'nt' else 'optionleft'
hexToText = lambda x: '+' + x if os.name == 'nt' else x
type_lock = threading.Lock()
def type_internal(text):
	with type_lock:
		ords = [ord(c) for c in text]
		if all(o < 128 for o in ords):
			pyautogui.write(text)
			return

		pyperclip.copy(text)
		pyautogui.hotkey("ctrl", "v")
		return

		#for o in ords:
		#	hex_txt = hexToText('%04x' % o)
		#	pyautogui.keyDown(hextypeKey)
		#	time.sleep(0.01)
		#	pyautogui.press([x for x in hex_txt])
		#	time.sleep(0.01)
		#	pyautogui.keyUp(hextypeKey)

get_data = lambda r: r.json or r.data

def try_redirecct_back():
	back_url = request.args.get('prev_page')
	if back_url is not None:
		return redirect(back_url)
	return 'ok'

@app.route('/template/<path:path>', methods=['GET'])
def template_get(path):
	if path == 'video_control':
		return redirect('/video_control', 301)
	temp_name = '%s.html' % path
	args_str = request.args.get('args')
	if args_str is not None:
		args_str = '{ %s }' % ','.join(('"%s": %s' % (k, v) for k, v in (x.split(':') for x in args_str.split(','))))
		args = eval(args_str)
		return render_template(temp_name, **args)
	return render_template(temp_name)

@app.route('/cmd', methods=['POST'])
def cmd_post():
	subprocess.run(get_data(request), shell=True)
	return 'ok'

@app.route('/click', methods=['POST'])
def click():
	x, y = request.args.get('x'), request.args.get('y')
	x, y = (float(x) if x else None, float(y) if y else None)

	pyautogui.click(x=x, y=y, clicks=int(request.args.get('count') or '1'), interval=float(request.args.get('interval') or '0.05'), button=request.args.get('button') or 'left')
	return 'ok'

@app.route('/move', methods=['POST'])
def move():
	threading.Timer(0, move_internal, [request.args.get('deltaX'), request.args.get('deltaY'), request.args.get('duration')]).start()
	return 'ok'

@app.route('/scroll', methods=['POST'])
def scroll():
	pyautogui.scroll(int(float(request.args.get('deltaY'))))
	return 'ok'

@app.route('/press', methods=['POST'])
def press_post():
	threading.Timer(0, press_internal, [get_data(request), request.args.get('repeats')]).start()
	return 'ok'

@app.route('/type', methods=['POST'])
def type_post():
	threading.Timer(0, type_internal, [get_data(request)]).start()
	return 'ok'

cur_w = 30
cur_h = 30
cur_img = Image.open('cur.cur')
cur_img.thumbnail((cur_w, cur_h), Image.ANTIALIAS)
screen_w = GetSystemMetrics(0)
screen_h = GetSystemMetrics(1)
@app.route('/screnshot', methods=['GET'])
def screnshot_get():
	cur_x, cur_y = pyautogui.position()
	delta_x, delta_y = int(request.args.get('delta_x') or '500'), int(request.args.get('delta_y') or '500')
	scale = float(request.args.get('scale') or '1')
	scaled_delta_x = int(scale * delta_x)
	scaled_delta_y = int(scale * delta_y)
	x = min(max(0, cur_x - scaled_delta_x), screen_w - 2 * scaled_delta_x)
	y = min(max(0, cur_y - scaled_delta_y), screen_h - 2 * scaled_delta_y)
	img = pyscreeze.screenshot(region=(x, y, 2 * scaled_delta_x, 2 * scaled_delta_y))

	if cur_x <= scaled_delta_x:
		img_cur_x = cur_x
	elif cur_x >= screen_w - scaled_delta_x:
		img_cur_x = 2 * scaled_delta_x + cur_x - screen_w
	else:
		img_cur_x = scaled_delta_x

	if cur_y <= scaled_delta_y:
		img_cur_y = cur_y
	elif cur_y >= screen_h - scaled_delta_y:
		img_cur_y = 2 * scaled_delta_y + cur_y - screen_h
	else:
		img_cur_y = scaled_delta_y

	img.paste(cur_img, (img_cur_x, img_cur_y), cur_img)

	if scale > 1:
		img.thumbnail((2 * delta_x, 2 * delta_y), Image.ANTIALIAS)

	rawBytes = io.BytesIO()
	img.save(rawBytes, "JPEG")
	rawBytes.seek(0)
	img_base64 = base64.b64encode(rawBytes.read())
	return jsonify({'img': 'data:image/png;base64, ' + img_base64.decode('UTF-8')})

@app.route('/video_control', methods=['GET'])
def video_control_get():
	return render_template('video_control.html', browser=request.user_agent.browser, get_hashed_path=get_hashed_path)

hashed_paths_cache: Dict[str, str] = {}
files_cache: Dict[str, str] = {}
def calculate_md5_and_store(path: str):
	bytes = open(path,'rb').read()
	file = bytes.decode('UTF-8')
	md5 = hashlib.md5(bytes).hexdigest()
	paths_list = list(os.path.splitext(path))
	paths_list[1] = '_' + md5 + paths_list[1]
	hashed_path = ''.join(paths_list)
	hashed_paths_cache[path] = hashed_path
	files_cache[hashed_path] = file

@app.route('/<dir_name>/<fname>')
def send_js(dir_name, fname):
	path = dir_name + '/' + fname
	file = files_cache[path]
	return file

def get_hashed_path(path):
	if len(path) == 0:
		raise Exception('path must be not empty')
	if path[0] == '/':
		path = path[1:]
	if not path in hashed_paths_cache:
		calculate_md5_and_store(path)
	return hashed_paths_cache[path]

@app.route('/favicon.ico')
def favicon():
	return send_file('favicon.ico', mimetype='image/webp')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
	return send_file('apple-touch-icon.png', mimetype='image/png')



if DEBUG:
	app.run(socket.gethostbyname(socket.gethostname()))
