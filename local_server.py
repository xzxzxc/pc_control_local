# coding=utf-8
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import os, datetime, pyautogui, sys, string, logging, time, socket, subprocess, re
from threading import Timer
from misc import user32Dll, allowed_keys, set_reg, get_reg, chunks, update_cur

app = Flask(__name__)
# logging.basicConfig(filename='log.txt', level=logging.DEBUG)
pyautogui.FAILSAFE = False

flag_names = ['Arrow', 'Help', 'AppStarting', 'Wait', 'Crosshair', 'IBeam', 'NWPen', 'No', 'SizeNS', 'SizeWE', 'SizeNWSE', 'SizeNESW', 'SizeAll', 'UpArrow', 'Hand']
new_flag_val = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cur.cur')
norm_values = {x: get_reg(x) for x in flag_names}

def move_inner(deltaX, deltaY, duration):
	deltaX, deltaY, duration = float(deltaX), float(deltaY), float(duration or '0.1')
	for flag_name in flag_names:
		set_reg(flag_name, new_flag_val)
	update_cur()
	pyautogui.moveRel(deltaX, deltaY, duration=duration)
	for flag_name in flag_names:
		set_reg(flag_name, norm_values[flag_name])
	Timer(0.8, update_cur).start()

def try_redirecct_back():
	back_url = request.args.get('prev_page')
	if back_url is not None:
		return redirect(back_url)
	return 'ok'

@app.route('/template/<path:path>', methods=['GET'])
def turnOff_get(path):
	temp_name = '%s.html' % path
	args_str = request.args.get('args')
	if args_str is not None:
		args_str = '{ %s }' % ','.join(('"%s": %s' % (k, v) for k, v in (x.split(':') for x in args_str.split(','))))
		args = eval(args_str)
		return render_template(temp_name, **args)
	return render_template(temp_name)

@app.route('/cmd/<path:command>', methods=['POST'])
def turnOff_post(command):
	subprocess.run(command, shell=True)
	return 'ok'

@app.route('/click', methods=['POST'])
def click():
	x, y = request.args.get('x'), request.args.get('y')
	x, y = (float(x) if x else None, float(y) if y else None)

	pyautogui.click(x=x, y=y, clicks=int(request.args.get('count') or '1'), interval=float(request.args.get('interval') or '1'))
	return 'ok'

@app.route('/move', methods=['POST'])
def move():
	Timer(0, move_inner, [request.args.get('deltaX'), request.args.get('deltaY'), request.args.get('duration')]).start()
	return 'ok'

@app.route('/press', methods=['POST'])
def press_post():
	key_sets = request.args.get('keys').split(';')
	for k_set in key_sets:
		pyautogui.hotkey(*k_set.split('+'))
		time.sleep(.250)
	return 'ok'

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)

if __name__ == '__main__':
	app.run(socket.gethostbyname(socket.gethostname()))
