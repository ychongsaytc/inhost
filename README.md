
# Inhost

A lightweight script helps you to deploy your server via web hooks.

- **License**: [GNU General Public License, version 2](http://www.gnu.org/licenses/gpl-2.0.html)

## Requirements

- [Python](https://www.python.org/) 2.7+
- [web.py](http://webpy.org/) 0.3+

## Quick Start

1. [Download the latest version of Inhost](https://github.com/ychongsaytc/inhost/releases)
2. Make your configuration for Inhost placed in `/config.json`
3. Run `python service.py start`
4. Visit `http://your-host:your-port/your-secret/the-command-set-id/` to process the deployment

## Configuration

The sample configuration can be found in `/config-sample.json`

### Options

- **http_host** (string)

	Hostname to listen. Required. Defaults to `'0.0.0.0'`.

- **http_port** (integer)

	Hostname to listen. Required. Defaults to `8787`.

- **url_secret** (string)

	The secret hash string in hook URL, please fill with your random string before production. Required.

- **pid_file** (string)

	File to store service PID. Required. Defaults to `'/var/run/inhost.pid'`.

- **log_file** (string)

	File to log. Required. Defaults to `'/var/log/inhost.log'`.

- **mail_setup** (name/value pairs)

	Outgoing mail service outgoing settings. Optional if mail notice not used.

	- **smtp_host** (string)

		The SMTP server name or IP. Defaults to `'localhost'`.

	- **smtp_port** (integer)

		The SMTP server port. Defaults to `25`.

	- **smtp_user** (string)

		The SMTP logging username.

	- **smtp_pass** (string)

		The SMTP logging password.

	- **smtp_ssl** (boolean)

		Using SSL to connect SMTP server. Defaults to `False`.

- **commands** (name/value pairs)

	The command sets.

	- **`{COMMAND_SET_ID}`** (name/value pairs)

		A command set.

		- **command** (string)

			A shell command to be executed.

		- **timeout** (integer|boolean)

			Maximum time in seconds to limit. Optional.

		- **mail_notice** (array:string|string)

			Receiver to send executing result notice. Optional.

## Usage

### Service controller

- Start: `python service.py start`
- Stop: `python service.py stop`
- Restart: `python service.py restart`

### Web Hook

Hook URL format: `http://HTTP_HOST:HTTP_PORT/URL_SECRET/THE_COMMAND_SET_ID/`

Refer to configuration parameters.

## Examples

#### Auto deploy website from Git repository

```json
{
	"commands": {
		"deploy_web": {
			"command": "service nginx stop; cd /var/www/html; git pull; composer update; bower update --allow-root; service nginx start",
			"timeout": 120,
			"mail_notice": [ "developer@example.com", "webmaster@example.com" ]
		}
	}
}
```

In this example Inhost will perform:

1. Stop nginx server
2. Change working directory to `/var/www/html`
3. Pull files from Git repository
4. Update Composer components
5. Update Bower components
6. Start nginx server

The command will be terminated if it takes more than 2 minutes.

## Reference

- [web.py Install guide](http://webpy.org/install)

---

Copyright &copy; 2015 [Yuan Chong](http://chon.io/)

