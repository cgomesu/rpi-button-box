#!/usr/bin/python3
from gpiozero import Button, Buzzer, Device, pi_info
from gpiozero.pins.mock import MockFactory
from gpiozero.tools import all_values, any_values
# see signal for handling SIGINT
from signal import pause
from argparse import ArgumentParser
# from subprocess import Popen, check_call
# the following is required for keyboard input mode
from pynput.keyboard import Key, Listener


# TODO: add logging once everything is working
def cli_args():
	ap = ArgumentParser(description='RPi button box controller.')
	ap.add_argument('--input', type=str, default='buttons', choices=['buttons', 'keyboard'], required=False,
					help='User input method. Default = buttons')
	ap.add_argument('--buzzer', type=int, default=None,
					choices=[2, 3, 4, 17, 27, 22, 10, 9, 11, 14, 15, 18, 23, 24, 25, 8, 7], required=False,
					help='GPIO# for an active buzzer. Default = None')
	ap.add_argument('--info', type=str, default=False, choices=['True', 'False'], required=False,
					help='Just print the board and headers information. Default = False')
	return vars(ap.parse_args())


# edit here if changing pins and keyboard keys
def config_buttons():
	if args['input'] is 'keyboard':
		Device.pin_factory = MockFactory()
	# set new Button class attributes
	Button.key, Button.type = '', ''
	# create Button devices and set their new attributes
	g1, g1.key, g1.type = Button(26), 1, 'push'
	b1, b1.key, b1.type = Button(19), 2, 'push'
	r1, r1.key, r1.type = Button(13), 3, 'push'
	g2, g2.key, g2.type = Button(6), 4, 'push'
	b2, b2.key, b2.type = Button(5), 5, 'push'
	r2, r2.key, r2.type = Button(12), 6, 'push'
	s1, s1.key, s1.type = Button(16, hold_time=2), 7, 'switch'
	s2, s2.key, s2.type = Button(20, hold_time=2), 8, 'switch'
	s3, s3.key, s3.type = Button(21, hold_time=2), 9, 'switch'
	return [g1, b1, r1, g2, b2, r2, s1, s2, s3]


def end(msg=None, status=0):
	# cleanup()
	print('Ending the program with the following message:\n{}\n'.format(msg))
	exit(status)


def event_held():
	print('event held')


def event_press():
	print('event press')


def event_release():
	print('event release')


# user input collector
def keyboard_collector(btns):
	with Listener(on_press=keyboard_press, on_release=keyboard_release, suppress=True):
		print('#################################################')
		print('################# KEYBOARD MODE #################')
		print('#################################################')
		print('Use your keyboard keys to simulate the button box.'
			'\n\nTo EXIT, press the \"ESC\" key.'
			'\nButton : Key mappings:\n')
		for btn in btns:
			print('* {0} : {1}'.format(btn.pin, btn.key))
		print('\n#################################################\nWaiting for an input...')
		Listener.join()


def keyboard_press(key):
	if key is Key.esc:
		end(msg='User pressed Escape in keyboard input mode', status=0)
	print('Pressing key: {}'.format(key))


def keyboard_release(key):
	print('Releasing key: {}'.format(key))


def main():
	# config_logging()
	buttons = config_buttons()
	if args['buzzer']:
		buzzer, buzzer.source = Buzzer(args['buzzer']), any_values(buttons)
	for button in buttons:
		if button.type is 'switch':
			button.when_held = event_held
		else:
			button.when_pressed, button.when_released = event_press, event_release
	pause() if args['input'] is 'buttons' else keyboard_collector(buttons)


if '__name__' == '__main__':
	args = cli_args()
	print('{0:board}\n0:headers'.format(pi_info())) if args['info'] else main()
	exit(0)
