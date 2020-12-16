#!/usr/bin/python3
from gpiozero import Button, Buzzer, pi_info
from gpiozero.tools import any_values
from signal import pause
from argparse import ArgumentParser
# from subprocess import Popen, check_call


# TODO(cgomesu): add logging capabilities
def cli_args():
	ap = ArgumentParser(description='RPi button box controller.')
	ap.add_argument('--buzzer', type=int, required=False, help='if installed, the buzzer\'s GPIO number.')
	ap.add_argument('-i', '--info', action='store_true', required=False, help='Just print the board information.')
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
	s1, s1.label, s1.type = Button(16, hold_time=2), 'power', 'switch'
	s2, s2.label, s2.type = Button(20, hold_time=2), 'middle S2', 'switch'
	s3, s3.label, s3.type = Button(21, hold_time=2), 'right S3', 'switch'
	return [g1, b1, r1, g2, b2, r2, s1, s2, s3]


def end(msg=None, status=0):
	# cleanup()
	print('Ending the program with the following message:\n{}\n'.format(msg))
	exit(status)


# edit event_* to what to do when a button is active or not
# btn.attributes can be used to assign events on a per button basis
def event_held(btn):
	print('event held')
	print('{0}\t{1}\t{2}'.format(btn.pin, btn.type, btn.label))


def event_press(btn):
	print('event press')
	print('{0}\t{1}\t{2}'.format(btn.pin, btn.type, btn.label))


def event_release(btn):
	print('event release')
	print('{0}\t{1}\t{2}'.format(btn.pin, btn.type, btn.label))
	if btn.label == 'power':
		end(msg='Power button ({}) is not being held anymore. Turning OFF.'.format(btn.pin), status=0)


def main():
	buttons = config_buttons()
	# wait for a button labelled 'power' to be turned ON before continuing
	try:
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
				button.when_held, button.when_released = event_held, event_release
			else:
				# assumes only 'push' and 'switch' types
				push_buttons.append(button)
				button.when_pressed, button.when_released = event_press, event_release
		if args['buzzer']:
			# buzzer is activated by any push button
			buzzer, buzzer.source = Buzzer(args['buzzer']), any_values(*push_buttons)
		print('The button box is now turned ON. To close it, release the power switch or press Ctrl+C.')
		pause()
	except Exception as err:
		end(msg='{}'.format(err), status=1)


if __name__ == '__main__':
	args = cli_args()
	print('{0:full}'.format(pi_info())) if args['info'] else main()
