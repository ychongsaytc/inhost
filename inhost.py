#!/usr/bin/env python


import os
import sys
import subprocess
import web

import core


urls = (
	'/', 'index',
	'/(\S+?)/(\S+?)/?', 'deploy',
)


class index:

	def GET ( self ) :
		return '<a href="https://github.com/ychongsaytc/inhost">Inhost</a> is installed on the server, which is a lightweight script that helps you to deploy you web server via web hooks.'


class deploy:

	def GET ( self, the_secret, the_command ) :
		config = core.get_config()
		# secret incorrect
		if the_secret != config['url_secret'] :
			return 'Access denied.'
		# command set does not exist
		if the_command not in config['commands'].keys() :
			return 'Command does not exist.'
		command_set = config['commands'][the_command]
		command = command_set['command']
		# run command and save output
		proc = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
		core.write_log( '[Inhost] Runing command "' + command + '" with PID: ' + str( proc.pid ) + ' ...', False )
		# wait for process end
		os.waitpid( proc.pid, 0 )
		# retrieve output
		proc_out, proc_err = proc.communicate()
		# write output to log
		core.write_log( '[Inhost] Command STDOUT:\n' + proc_out, False )
		core.write_log( '[Inhost] Command STDERR:\n' + proc_err, False )
		# send output as notice email
		if True == command_set['email_notice'] :
			mail_receiver = config['email']['receiver']
			mail_message = ''.join( [
					'<h3>Detials</h3>',
					'<p><strong>Command:</strong></p>',
					'<pre><code>' + command + '</code></pre>',
					'<p><strong>STDOUT:</strong></p>',
					'<pre><code>' + proc_out + '</code></pre>',
					'<p><strong>STDERR:</strong></p>',
					'<pre><code>' + proc_err + '</code></pre>',
					'<hr />',
					'<p><small>This mail was sent by Inhost robot, please do not reply directly.</small></p>',
				] )
			core.write_log( '[Inhost] Sending command result email to ' + str( mail_receiver ) + ' ...', False )
			try:
				core.send_email( mail_receiver, 'The command has been processed', mail_message )
				core.write_log( '[Inhost] Command result has been sent to ' + str( mail_receiver ), False )
			except:
				core.write_log( '[Inhost] Send mail error: ' + str( sys.exc_info()[1] ), False )
		return 'Done.'

	def POST ( self, the_secret, the_command ) :
		return self.GET( the_secret, the_command )


class web_app ( web.application ) :

	def run ( self, host, port, *middleware ) :
		func = self.wsgifunc( *middleware )
		return web.httpserver.runsimple( func, ( host, port ) )


if __name__ == '__main__' :
	config = core.get_config()
	app = web_app( urls, globals() )
	app.run( config['http_host'], config['http_port'] )

