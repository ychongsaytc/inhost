#!/usr/bin/env python


import os
import sys
import signal
import subprocess
import argparse

import core


config = core.get_config()


def service_start() :
	core.write_log( '[Inhost] Staring Inhost ...', True )
	if os.path.isfile( config['pid_file'] ) :
		# pid file already exists
		core.write_log( '[Inhost] Inhost has been started already.', True )
	else :
		# set as process group leader
		os.setpgrp()
		try:
			# open `/dev/null` as stream
			FNULL = open( os.devnull, 'w' )
			# run Inhost web server process via shell
			proc = subprocess.Popen( 'python ' + os.path.dirname( os.path.abspath( __file__ ) ) + '/inhost.py', stdout=FNULL, stderr=FNULL, shell=True )
		except:
			core.write_log( '[Inhost] Error: ' + str( sys.exc_info()[1] ), True )
		# write pid
		with open( config['pid_file'], 'w+' ) as the_file :
			the_file.write( str( proc.pid ) )
			the_file.close()
		core.write_log( '[Inhost] OK, Inhost is running with PID ' + str( proc.pid ) + ', PGID ' + str( os.getpgid( proc.pid ) ) + '.', True )


def service_stop() :
	core.write_log( '[Inhost] Stopping Inhost ...', True )
	if not os.path.isfile( config['pid_file'] ) :
		# pid file does not exist
		core.write_log( '[Inhost] Inhost not started.', True )
	else :
		# get pid from temporarily file
		with open( config['pid_file'], 'r' ) as the_file :
			pid = the_file.read()
		try:
			# get pgid of Inhost web server process
			pgid = os.getpgid( int( pid ) )
			# kill web server process
			os.kill( int( pid ), signal.SIGQUIT )
			# ... and its child processes
			os.killpg( int( pgid ), signal.SIGQUIT )
		except:
			core.write_log( '[Inhost] Error: ' + str( sys.exc_info()[1] ), True )
		# remove temporarily file
		os.remove( config['pid_file'] )
		core.write_log( '[Inhost] OK.', True )


if None != config :
	parser = argparse.ArgumentParser( description='Inhost Controller' )
	parser.add_argument( 'action', metavar='<action>', type=str, choices=[ 'start', 'stop', 'restart'], help='action to process' )
	args = parser.parse_args()
	if args.action == 'start' :
		service_start()
	elif args.action == 'stop' :
		service_stop()
	elif args.action == 'restart' :
		service_stop()
		service_start()

