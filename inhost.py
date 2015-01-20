#!/usr/bin/env python


import os
import sys
import subprocess
import threading
import time
import signal
import web

import core


config = core.get_config()

urls = (
	'/', 'index',
	'/(\S+?)/(\S+?)/?', 'deploy',
)


class index:

	def GET ( self ) :
		return '<a href="https://github.com/ychongsaytc/inhost" target="_blank">Inhost</a> is installed on the server, which is a lightweight script that helps you to deploy you web server via web hooks.'


class deploy:

	def GET ( self, the_secret, the_command ) :
		# secret incorrect
		if the_secret != config['url_secret'] :
			return 'Access denied.'
		# command set does not exist
		if the_command not in config['commands'].keys() :
			return 'Command does not exist.'
		command_set = config['commands'][the_command]
		command = command_set['command']
		proc_status = 'Successful'
		time_start = time.time()
		# run command and save output
		proc = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid )
		core.write_log( '[Inhost] Runing command "' + command + '" with PID: ' + str( proc.pid ) + ' ...' )
		# set up timer for timeout
		timeout = command_set['timeout']
		def timer_timeout() :
			core.write_log( '[Inhost] Waiting for ' + str( timeout ) + ' seconds ...' )
			time.sleep( timeout )
			if None == proc.poll() :
				core.write_log( '[Inhost] Time out, terminating ...' )
				# kill the command process group
				os.killpg( os.getpgid( proc.pid ), signal.SIGQUIT )
				proc_status = 'Timeout'
		thread = threading.Thread( target=timer_timeout )
		thread.start()
		# wait for process end then retrieve output
		proc_out, proc_err = proc.communicate()
		time_elapsed = time.time() - time_start
		# filter illegal unicode characters
		proc_out = unicode( proc_out, encoding='ascii', errors='ignore' )
		# write output to log
		core.write_log( '[Inhost] Command output:\n' + proc_out )
		# send output as notice email
		if command_set['mail_notice'] :
			mail_receiver = command_set['mail_notice']
			if type('') == type( mail_receiver ) :
				mail_receiver = [ mail_receiver ]
			mail_subject = 'The command has been processed'
			mail_message = ''.join( [
					'<h3>Result: ' + proc_status + '</h3>',
					'<p><strong>Time elapsed:</strong></p>',
					'<pre>' + ( '%.2f' % time_elapsed ) + ' second(s)</pre>',
					'<p><strong>Command:</strong></p>',
					'<pre><code>' + command + '</code></pre>',
					'<p><strong>Output:</strong></p>',
					'<pre><code>' + proc_out + '</code></pre>',
				] )
			core.write_log( '[Inhost] Sending command result email to ' + ', '.join( mail_receiver ) + ' ...' )
			try:
				core.send_email( mail_receiver, mail_subject, mail_message )
				core.write_log( '[Inhost] Command result has been sent to ' + ', '.join( mail_receiver ) )
			except:
				core.write_log( '[Inhost] Send mail error: ' + str( sys.exc_info()[1] ) )
		return 'Done.'

	def POST ( self, the_secret, the_command ) :
		return self.GET( the_secret, the_command )


class web_app ( web.application ) :

	def run ( self, host, port, *middleware ) :
		func = self.wsgifunc( *middleware )
		return web.httpserver.runsimple( func, ( host, port ) )


if __name__ == '__main__' :
	if None != config :
		app = web_app( urls, globals() )
		app.run( config['http_host'], config['http_port'] )

