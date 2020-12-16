#!/usr/bin/python3
from gpiozero import Button, Buzzer, pi_info
from gpiozero.tools import any_values
from signal import pause
from argparse import ArgumentParser
from subprocess import Popen, run
from time import sleep


# TODO(cgomesu): add logging capabilities
def cli_args():
	ap = ArgumentParser(description='RPi button box controller. Repo: https://github.com/cgomesu/rpi-button-box')
	ap.add_argument('--buzzer', type=int, required=False, help='\tIf installed, the buzzer\'s GPIO number.')
	ap.add_argument('--cmd', type=str, required=False, choices=['Popen', 'run'], default='Popen',
					help='\tPopen: invoke external scripts in a NON-BLOCKING fashion. '
						'run: invoke external scripts in a BLOCKING fashion. Default=Popen')
	ap.add_argument('--g1_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button G1 is pressed. Default=None')
	ap.add_argument('--g1_released', type=str, required=False, default=None,
					help='Path to the script to run when the button G1 is released. Default=None')
	ap.add_argument('--b1_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button B1 is pressed. Default=None')
	ap.add_argument('--b1_released', type=str, required=False, default=None,
					help='Path to the script to run when the button B1 is released. Default=None')
	ap.add_argument('--r1_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button R1 is pressed. Default=None')
	ap.add_argument('--r1_released', type=str, required=False, default=None,
					help='Path to the script to run when the button R1 is released. Default=None')
	ap.add_argument('--g2_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button G2 is pressed. Default=None')
	ap.add_argument('--g2_released', type=str, required=False, default=None,
					help='Path to the script to run when the button G2 is released. Default=None')
	ap.add_argument('--b2_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button B2 is pressed. Default=None')
	ap.add_argument('--b2_released', type=str, required=False, default=None,
					help='Path to the script to run when the button B2 is released. Default=None')
	ap.add_argument('--r2_pressed', type=str, required=False, default=None,
					help='Path to the script to run when the button R2 is pressed. Default=None')
	ap.add_argument('--r2_released', type=str, required=False, default=None,
					help='Path to the script to run when the button R2 is released. Default=None')
	ap.add_argument('--s1_held', type=str, required=False, default=None,
					help='Path to the script to run when the button S1 is held. Default=None')
	ap.add_argument('--s1_released', type=str, required=False, default=None,
					help='Path to the script to run when the button S1 is released. Default=None')
	ap.add_argument('--s2_held', type=str, required=False, default=None,
					help='Path to the script to run when the button S2 is held. Default=None')
	ap.add_argument('--s2_released', type=str, required=False, default=None,
					help='Path to the script to run when the button S2 is released. Default=None')
	ap.add_argument('--s3_held', type=str, required=False, default=None,
					help='Path to the script to run when the button S3 is held. Default=None')
	ap.add_argument('--s3_released', type=str, required=False, default=None,
					help='Path to the script to run when the button S3 is released. Default=None')
	ap.add_argument('-i', '--info', action='store_true', required=False, help='Just print the board information.')
	ap.add_argument('-d', '--debug', action='store_true', required=False, help='Prints events to the terminal.')
	return vars(ap.parse_args())


# edit here if changing pins and labels
def config_buttons():
	# set new Button class attributes
	Button.label, Button.type, Button.cmdheld, Button.cmdpressed, Button.cmdreleased = False, False, False, False, False
	# create Button devices and set their new attributes
	g1, g1.label, g1.type, g1.cmdpressed, g1.cmdreleased = Button(26), 'green #1', 'push', args['g1_pressed'], args['g1_released']
	b1, b1.label, b1.type, b1.cmdpressed, b1.cmdreleased = Button(19), 'black #1', 'push', args['b1_pressed'], args['b1_released']
	r1, r1.label, r1.type, r1.cmdpressed, r1.cmdreleased = Button(13), 'red #1', 'push', args['r1_pressed'], args['r1_released']
	g2, g2.label, g2.type, g2.cmdpressed, g2.cmdreleased = Button(6), 'green #2', 'push', args['g2_pressed'], args['g2_released']
	b2, b2.label, b2.type, b2.cmdpressed, b2.cmdreleased = Button(5), 'black #2', 'push', args['b2_pressed'], args['b2_released']
	r2, r2.label, r2.type, r2.cmdpressed, r2.cmdreleased = Button(12), 'red #2', 'push', args['r2_pressed'], args['r2_released']
	s1, s1.label, s1.type, s1.cmdheld, s1.cmdreleased = Button(16, hold_time=2), 'power', 'switch', args['s1_held'], args['s1_released']
	s2, s2.label, s2.type, s2.cmdheld, s2.cmdreleased = Button(20, hold_time=2), 'middle S2', 'switch', args['s2_held'], args['s2_released']
	s3, s3.label, s3.type, s3.cmdheld, s3.cmdreleased = Button(21, hold_time=2), 'right S3', 'switch', args['s3_held'], args['s3_released']
	return [g1, b1, r1, g2, b2, r2, s1, s2, s3]


def end(msg=None, status=0):
	if not msg:
		msg = 'There\'s no message'
	if args['debug']:
		print('Ending the program with the following message:\n{}\n'.format(msg))
	exit(status)


# btn.attributes can be used to assign events on a per button basis
def event_held(btn):
	if args['debug']:
		print('Detected a HELD event by {0} : {1} button : {2}'.format(btn.pin, btn.type, btn.label))
	if btn.cmdheld:
		Popen(btn.cmdheld) if args['cmd'] == 'Popen' else run(btn.cmdheld)
		if args['debug']:
			print('Finished invoking the script at \'{}\''.format(btn.cmdheld))


def event_pressed(btn):
	if args['debug']:
		print('Detected a PRESS event by {0} : {1} button : {2}'.format(btn.pin, btn.type, btn.label))
	if btn.cmdpressed:
		Popen(btn.cmdpressed) if args['cmd'] == 'Popen' else run(btn.cmdpressed)
		if args['debug']:
			print('Finished invoking the script at \'{}\''.format(btn.cmdpressed))
	sleep(0.05)  # add 50ms to prevent accidental re-triggers


def event_released(btn):
	if args['debug']:
		print('Detected a RELEASE event by {0} : {1} button : {2}'.format(btn.pin, btn.type, btn.label))
	if btn.label == 'power':
		end(msg='The power button ({}) was released from the ON state.'.format(btn.pin), status=0)
	elif btn.cmdreleased:
		Popen(btn.cmdheld) if args['cmd'] == 'Popen' else run(btn.cmdheld)
		if args['debug']:
			print('Finished invoking the script at \'{}\''.format(btn.cmdheld))
	sleep(0.05)  # add 50ms to prevent accidental re-triggers


def main():
	buttons = config_buttons()
	# wait for a button labelled 'power' to be turned ON before continuing
	for button in buttons:
		if button.label == 'power':
			if not button.is_held:
				print('Waiting for the power button ({}) to be turned on ...'.format(button.pin))
				button.wait_for_active()
			break
	# when_* properties will pass the device that activated it to a function that takes a single parameter
	# use the device's attributes (e.g., pin, type, label) to determine what to do
	push_buttons, switches = [], []
	for button in buttons:
		if button.type == 'switch':
			switches.append(button)
			button.when_held, button.when_released = event_held, event_released
		else:
			# assumes only 'push' and 'switch' types
			push_buttons.append(button)
			button.when_pressed, button.when_released = event_pressed, event_released
	if args['buzzer']:
		# buzzer is activated by any push button
		buzzer, buzzer.source = Buzzer(args['buzzer']), any_values(*push_buttons)
	print('The button box is now turned ON. To close it, release the power button or press Ctrl+C.')
	pause()


if __name__ == '__main__':
	args = cli_args()
	print('{0:full}'.format(pi_info())) if args['info'] else main()
