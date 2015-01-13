

import os
import json
import smtplib


def get_config() :
	# configuration file order
	if os.path.isfile( 'config.json' ) :
		stream = open( 'config.json' )
	elif os.path.isfile( '/etc/inhost/config.json' ) :
		stream = open( '/etc/inhost/config.json' ) 
	elif os.path.isfile( 'config-smaple.json' ) :
		stream = open( 'config-smaple.json' )
	else :
		write_log( '[Inhost] Configuration file does not exist.' )
		return
	the_conf = json.load( stream )
	return the_conf


def write_log( msg, to_print = True ) :
	config = get_config()
	# write to log file
	with open( config['log_file'], 'a+' ) as the_file :
		the_file.write( msg + '\n' )
		the_file.close()
	# print to STDOUT
	if to_print :
		print msg


def send_email( mail_receiver, mail_subject, mail_message ) :
	if type('') == type( mail_receiver ) :
		mail_receiver = [ mail_receiver ]
	config = get_config()
	mail_sender = config['email']['smtp_user']
	mail_message = '\r\n'.join( [
			'From: Inhost <' + mail_sender + '>',
			'To: ' + ', '.join( mail_receiver ),
			'MIME-Version: 1.0',
			'Content-Type: text/html',
			'Subject: ' + mail_subject,
			'',
			mail_message
		] )
	if config['email']['smtp_ssl'] :
		s = smtplib.SMTP_SSL()
	else :
		s = smtplib.SMTP()
	s.connect( config['email']['smtp_host'], config['email']['smtp_port'] )
	s.login( config['email']['smtp_user'], config['email']['smtp_pass'] )
	s.sendmail( mail_sender, mail_receiver, mail_message )
	s.close()

