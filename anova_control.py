#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Yeah, we need this shit
import sys
import anova
import argparse
import json
import time
import logging

#Constants
cooker_id = 'anova xxxxxxxxxxxxxxxxxxxx'
secret = 'yyyyyyyyyyyyyy'

#Setup the logging - depending on your setup this may need adjusted
logging.basicConfig(filename='/var/log/anova_control.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Script started')

#Used to properly parse the JSON output - this handles nulls in the data
def dictator(data, path=None, default=None, checknone=False):
    if path is None or path == '':
        return json.dumps(data)

    value = None
    keys = path.split(".")

    # reset path
    path = None

    # if 1st key is a list index
    if all(char.isdigit() for char in keys[0]):
        path = '['+keys[0]+']'

        # remove 1st key from key list
        keys.pop(0)

    # build proper path
    for key in keys:
        # check if key is a list
        if key.endswith(']'):
            temp = key.split('[')
            key = ''.join(temp[0])
            index = int(temp[1].strip(']'))
            if path is None:
                path = "['"+key+"']"+"["+str(index)+"]"
            else:
                path = path+"['"+key+"']"+"["+str(index)+"]"
        else:
            if path is None:
                path = "['"+key+"']"

            else:
                # check if key is an index
                if key.isdigit() is True:
                    path = path + "["+key+"]"
                else:
                    path = path + "['"+key+"']"
    lookup = 'data'+path
    try:
        value = eval(lookup)
        if value is None:
            value = default
    except (KeyError, ValueError, IndexError, TypeError) as err:
        value = default
    finally:
        if checknone:
            if not value:
                raise ValueError('missing value for %s' % path)
    return value

#Global check arguments function
def check_arg(args=None):
	#Set up all the possible command line arguments
    parser = argparse.ArgumentParser(description='Script to control Anova cooker')
    parser.add_argument('-m', '--method',
						type=str,
                        help='What method to call.',
						choices=['status', 'silence', 'start', 'stop', 'icebath'],
                        required='True')
    parser.add_argument('-t', '--temperature',
						type=int,
                        help='Set temperature (required when using "start")')
    parser.add_argument('-d', '--duration',
						type=int,
                        help='The duration to cook for in minutes. (required when using "start")')
    parser.add_argument('-u', '--unit',
						type=str,
                        help='The temperature unit (defaults to °f).',
						choices=['f', 'c'],
						default='f')
    parser.add_argument('-s', '--stopalarm',
						type=str,
                        help='Stops the alarm also when stopping cook (defaults to y).',
						choices=['y', 'n', 'yes', 'no'],
						default='y')
    parser.add_argument('-o', '--output',
						type=str,
                        help='Output type, RAW JSON or HA JSON (defaults to RAW JSON).  HA JSON is formatted for better injestion into Home Assistant.',
						choices=['r', 'h', 'raw', 'ha'],
						default='r')

    results = parser.parse_args(args)
    return (results.method,
            results.temperature,
            results.duration,
			results.unit,
			results.stopalarm,
			results.output)

if __name__ == '__main__':
	#Parse out all the arguments
	m, t, d, u, s, o = check_arg(sys.argv[1:])
	
	#Logging all the passed variables
	logging.info('Method is: %s', m)
	logging.info('Temp is: %s', t)
	logging.info('Duration is: %s', d)
	logging.info('Unit is: %s', u)
	logging.info('Stop alarm flag is: %s', s)
	logging.info('Output type is: %s', o)
	
	#Set up the connection to the cooker_id
	cooker = anova.AnovaCooker(cooker_id, secret)
	
	#Get the current cooker status
	cooker_status=cooker.get_status()
	parsed_json = json.loads(cooker_status)
	is_running=dictator(parsed_json, "status.is_running")

	#Core if statements base on method specified on the command line
	if m == "status" :
		logging.info('Calling method status')
		display=cooker.get_status()
	elif m == "silence" :
		logging.info('Calling method silence')
		display=cooker.stop_alarm()
	elif m == "stop":
		logging.info('Calling method stop')
		cooker.running = False
		if (s == "y") or (s == "yes"):
			display=cooker.stop_alarm()
		else:
			display=cooker.get_status()
		#Also stop the ice bath if it's running
		cooker.stop_ice_bath()
	elif m == "start":
		logging.info('Calling method start')
		#We need to ensure the required arguments are supplied
		if (t is None) or (d is None):
			logging.error('Start arguments missing')
			display="One or more required arguments are missing!  Run this program with the -h flag for help."
		else:
			#Check if cooker is already running
			if is_running != True:
				logging.info('Starting the cooker')
				cooker.create_job(t, d * 60, u) #This expects seconds so minutes * 60
				time.sleep(3) #Wait just a few seconds for the command to complete
				display=cooker.get_status()
			else:
				logging.arning('Cooker already running')
				display=cooker.get_status()
	elif m == "icebath":
		cooker.start_ice_bath(t)
		display=cooker.get_status()
	else:
		#We shouldn't ever hit this point
		logging.critical('Something realld bad happened')
		print("Something is broken")

#Which format of the JSON are we sending out
if (o == "r") or (o == "raw") :
	print(display)
else:
	#Parse out the JSON
	parsed_json = json.loads(display)
	current_temp=dictator(parsed_json, "status.current_temp")
	is_running=dictator(parsed_json, "status.is_running")
	is_timer_running=dictator(parsed_json, "status.is_timer_running")
	speaker_mode=dictator(parsed_json, "status.speaker_mode")
	target_temp=dictator(parsed_json, "status.target_temp")
	temp_unit=dictator(parsed_json, "status.temp_unit")
	timer_length=dictator(parsed_json, "status.timer_length")
	alarm_active=dictator(parsed_json, "status.alarm_active")
	job_type=dictator(parsed_json, "status.current_job.job_type")
	job_stage=dictator(parsed_json, "status.current_job.job_stage")
	job_start_time=dictator(parsed_json, "status.current_job.job_start_time")
	duration=dictator(parsed_json, "status.current_job.job_info.duration")
	
	#Build the new JSON into an array
	data = {}
	data['current_temp'] = current_temp
	data['is_running'] = is_running
	data['is_timer_running'] = is_timer_running
	data['speaker_mode'] = speaker_mode
	data['target_temp'] = target_temp
	data['temp_unit'] = temp_unit
	data['timer_length'] = timer_length
	data['alarm_active'] = alarm_active
	data['job_type'] = job_type
	data['job_stage'] = job_stage
	data['job_start_time'] = job_start_time
	data['duration'] = duration
	json_data = json.dumps(data)
	
	#Output the HA friendly JSON
	print(json_data)
	
logging.info('Script ending')
