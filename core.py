

import os
import json
import smtplib


def get_config() :
	abspath = os.path.dirname( os.path.abspath( __file__ ) )
	# configuration file order
	if os.path.isfile( abspath + '/config.json' ) :
		stream = open( abspath + '/config.json' )
	elif os.path.isfile( '/etc/inhost/config.json' ) :
		stream = open( '/etc/inhost/config.json' ) 
	elif os.path.isfile( abspath + '/config-smaple.json' ) :
		stream = open( abspath + '/config-smaple.json' )
	else :
		print '[Inhost] Configuration file does not exist.'
		return
	the_conf = json.load( stream )
	return the_conf


def write_log( msg, to_print = False ) :
	config = get_config()
	# write to log file
	with open( config['log_file'], 'a+' ) as the_file :
		the_file.write( msg + '\n' )
		the_file.close()
	# print to STDOUT
	if to_print :
		print msg


def send_email( mail_receiver, mail_subject, mail_message ) :
	config = get_config()
	mail_sender = config['mail_setup']['smtp_user']
	mail_message = '\r\n'.join( [
			'From: Inhost <' + mail_sender + '>',
			'To: ' + ', '.join( mail_receiver ),
			'MIME-Version: 1.0',
			'Content-Type: text/html',
			'Subject: ' + mail_subject,
			'',
			mail_message,
			''.join( [
					'<hr />',
					'<p><small>This mail was sent by <a href="https://github.com/ychongsaytc/inhost" target="_blank">Inhost</a> robot, please do not reply directly.</small></p>',
				] )
		] )
	if config['mail_setup']['smtp_ssl'] :
		s = smtplib.SMTP_SSL( None, None, None, None, None, 60 );
	else :
		s = smtplib.SMTP( None, None, None, 60 );
	s.connect( config['mail_setup']['smtp_host'], config['mail_setup']['smtp_port'] )
	s.login( config['mail_setup']['smtp_user'], config['mail_setup']['smtp_pass'] )
	s.sendmail( mail_sender, mail_receiver, mail_message )
	s.close()

