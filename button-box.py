#!/usr/bin/python3
from gpiozero import Button, Buzzer, pi_info
from gpiozero.tools import any_values
# see signal for handling SIGINT
from signal import pause
from argparse import ArgumentParser
# from subprocess import Popen, check_call


# TODO(cgomesu): add logging capabilities
def cli_args():
	ap = ArgumentParser(description='RPi button box controller.')
	ap.add_argument('--buzzer', type=int, default=None,
					choices=[2, 3, 4, 17, 27, 22, 10, 9, 11, 14, 15, 18, 23, 24, 25, 8, 7], required=False,
					help='GPIO# for an active buzzer. Default = None')
	ap.add_argument('--info', type=str, default=False, choices=['True', 'False'], required=False,
					help='Just print the board and headers information. Default = False')
	return vars(ap.parse_args())


# edit here if changing pins and labels
def config_buttons():
	# set new Button class attributes
	Button.label, Button.type = '', ''
	# create Button devices and set their new attributes
	g1, g1.label, g1.type = Button(26), 'green #1', 'push'
	b1, b1.label, b1.type = Button(19), 'black #1', 'push'
	r1, r1.label, r1.type = Button(13), 'red #1', 'push'
	g2, g2.label, g2.type = Button(6), 'green #2', 'push'
	b2, b2.label, b2.type = Button(5), 'black #2', 'push'
	r2, r2.label, r2.type = Button(12), 'red #2', 'push'
	s1, s1.label, s1.type = Button(16, hold_time=2), 'on/off S1', 'switch'
	s2, s2.label, s2.type = Button(20, hold_time=2), 'middle S2', 'switch'
	s3, s3.label, s3.type = Button(21, hold_time=2), 'right S3', 'switch'
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
	pause()


if __name__ == '__main__':
	args = cli_args()
	print('{0:board}\n0:headers'.format(pi_info())) if args['info'] else main()
