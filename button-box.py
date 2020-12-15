#!/usr/local/bin/python3.9
from gpiozero import Button, Buzzer, Device, pi_info
from gpiozero.pins.mock import MockFactory
from gpiozero.tools import any_values
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
	if args['input'] == 'keyboard':
		Device.pin_factory = MockFactory()
	# set new Button class attributes
	Button.key, Button.label, Button.type = '', '', ''
	# create Button devices and set their new attributes
	g1, g1.key, g1.label, g1.type = Button(26), 1, 'green #1', 'push'
	b1, b1.key, b1.label, b1.type = Button(19), 2, 'black #1', 'push'
	r1, r1.key, r1.label, r1.type = Button(13), 3, 'red #1', 'push'
	g2, g2.key, g2.label, g2.type = Button(6), 4, 'green #2', 'push'
	b2, b2.key, b2.label, b2.type = Button(5), 5, 'black #2', 'push'
	r2, r2.key, r2.label, r2.type = Button(12), 6, 'red #2', 'push'
	s1, s1.key, s1.label, s1.type = Button(16, hold_time=2), 7, 'on/off S1', 'switch'
	s2, s2.key, s2.label, s2.type = Button(20, hold_time=2), 8, 'middle S2', 'switch'
	s3, s3.key, s3.label, s3.type = Button(21, hold_time=2), 9, 'right S3', 'switch'
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
	with Listener(on_press=keyboard_press, on_release=keyboard_release, suppress=True) as listener:
		print('#################################################')
		print('################# KEYBOARD MODE #################')
		print('#################################################')
		print('Use your keyboard keys to simulate the button box.'
			'\n\nTo EXIT, press the \"ESC\" key.'
			'\n\n\'Button : GPIO# : Key\' mappings:')
		for btn in btns:
			print('*{0}\t:\t{1}\t:\t{2}'.format(btn.label, btn.pin, btn.key))
		print('\n#################################################\nWaiting for an input...')
		listener.join()


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
		if button.type == 'switch':
			button.when_held = event_held
		else:
			button.when_pressed, button.when_released = event_press, event_release
	pause() if args['input'] == 'buttons' else keyboard_collector(buttons)


if __name__ == '__main__':
	args = cli_args()
	print('{0:board}\n0:headers'.format(pi_info())) if args['info'] else main()

