#!/usr/bin/env python


import os
import sys
import signal

import core


core.write_log( '[Inhost] Stopping Inhost ...' )

config = core.get_config()

if None != config :
	if not os.path.isfile( config['pid_file'] ) :
		# pid file does not exist
		core.write_log( '[Inhost] Inhost not started.' )
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
			core.write_log( '[Inhost] Error: ' + str( sys.exc_info()[1] ) )
		# remove temporarily file
		os.remove( config['pid_file'] )
		core.write_log( '[Inhost] OK.' )

