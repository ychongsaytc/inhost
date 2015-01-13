#!/usr/bin/env python


import os
import subprocess

import core


core.write_log( '[Inhost] Staring Inhost ...' )

config = core.get_config()

if None != config :
	if os.path.isfile( config['pid_file'] ) :
		# pid file already exists
		core.write_log( '[Inhost] Inhost has been started already.' )
	else :
		# set as process group leader
		os.setpgrp()
		try:
			# open `/dev/null` as stream
			FNULL = open( os.devnull, 'w' )
			# run Inhost web server process via shell
			proc = subprocess.Popen( 'python inhost.py', stdout=FNULL, stderr=FNULL, shell=True )
		except:
			core.write_log( '[Inhost] Error: ' + str( sys.exc_info()[1] ) )
		# write pid
		with open( config['pid_file'], 'w+' ) as the_file :
			the_file.write( str( proc.pid ) )
			the_file.close()
		core.write_log( '[Inhost] OK, Inhost is running with PID ' + str( proc.pid ) + ', PGID ' + str( os.getpgid( proc.pid ) ) + '.' )

