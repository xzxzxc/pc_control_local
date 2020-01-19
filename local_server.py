# coding=utf-8
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import os, datetime, pyautogui, sys, string, logging, time, socket, subprocess, re
from threading import Timer
from misc import user32Dll, allowed_keys, set_reg, get_reg, chunks, update_cur

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
	Timer(0.8, update_cur).start()

def press_internal(keys, repeats):
	key_sets = keys.split(';')
	for _ in range(min(int(repeats or 1), 25)):
		for k_set in key_sets:
			pyautogui.hotkey(*k_set.split('+'))
			time.sleep(.01)

def try_redirecct_back():
	back_url = request.args.get('prev_page')
	if back_url is not None:
		return redirect(back_url)
	return 'ok'

@app.route('/template/<path:path>', methods=['GET'])
def template_get(path):
	temp_name = '%s.html' % path
	args_str = request.args.get('args')
	if args_str is not None:
		args_str = '{ %s }' % ','.join(('"%s": %s' % (k, v) for k, v in (x.split(':') for x in args_str.split(','))))
		args = eval(args_str)
		return render_template(temp_name, **args)
	return render_template(temp_name)

@app.route('/cmd/<path:command>', methods=['POST'])
def cmd_post(command):
	subprocess.run(command, shell=True)
	return 'ok'

@app.route('/click', methods=['POST'])
def click():
	x, y = request.args.get('x'), request.args.get('y')
	x, y = (float(x) if x else None, float(y) if y else None)

	pyautogui.click(x=x, y=y, clicks=int(request.args.get('count') or '1'), interval=float(request.args.get('interval') or '0.05'), button=request.args.get('button') or 'left')
	return 'ok'

@app.route('/move', methods=['POST'])
def move():
	Timer(0, move_internal, [request.args.get('deltaX'), request.args.get('deltaY'), request.args.get('duration')]).start()
	return 'ok'

@app.route('/scroll', methods=['POST'])
def scroll():
	pyautogui.scroll(int(float(request.args.get('deltaY'))))
	return 'ok'

@app.route('/press', methods=['POST'])
def press_post():
	Timer(0, press_internal, [request.args.get('keys'), request.args.get('repeats')]).start()
	return 'ok'

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)

@app.after_request
def add_header(r):
	if not DEBUG:
		return r
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	return r

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('', 'favicon.ico', mimetype='image/webp')

if DEBUG:
	app.run(socket.gethostbyname(socket.gethostname()))
