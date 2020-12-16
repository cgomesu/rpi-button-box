#!/bin/bash

######################################
# Template for a button shell script #
#######################################################################
# Note 01.	Proper use of exit statuses is key if using this script in 
# 			conjunction with Python's subprocess.run() or check
#######################################################################


##########################
# script functions go here
cleanup () {
	echo 'Cleaning up...'
	# if necessary, add cleanup procedure here. it's called by end.
	echo 'Finished cleanup.'
}

# call `end` to exit the script with `msg` ($1) and `status` ($2) as args.
# for example, to finish the program with a successful message and `exit 0` status:
# end 'Finished running successfully' 0
end () {
	local message; local status
	if [[ -z "$1" ]]; then message='Message not provided'; else message="$1"; fi
	if [[ -z "$2" || ! "$2" =~ [0-9]{1,3} ]]; then status=1; else status=$2; fi
	echo 'Closing a button shell script with the following message:'; echo "- $message"
	# cleanup # uncomment cleanup if using it
	exit $status
}

start () {
	echo 'Started a button shell script.'
	# add shell commands here; depending on usage, edit `cleanup`
}


########################
# script logic goes here
trap 'end "Received a signal to stop." 1'  SIGINT SIGTERM SIGHUP

start 
# if necessary, add call to other functions here

end 'Reached EOF' 0
