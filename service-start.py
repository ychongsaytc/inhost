#!/usr/bin/env python


import os
import subprocess

import core


config = core.get_config()

if None != config :
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

