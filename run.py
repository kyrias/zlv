#!/usr/bin/env python
from flask import Flask, send_from_directory, render_template, url_for
from urllib.parse import quote_plus
import sys, os
class Network():
	name = ''
	url  = ''
	channels = []
	def __init__(self, name, url, channels):
		self.name     = name
		self.url      = url
		self.channels = channels
class Channel():
	name = ''
	url  = ''
	logs = []
	def __init__(self, name, url, logs):
		self.name = name
		self.url  = url
		self.logs = logs
class Log():
	name = ''
	url  = ''
	def __init__(self, name, url):
		self.name = name
		self.url  = url

app = Flask(__name__)
app.jinja_env.add_extension('jinja2_highlight.HighlightExtension')
app.jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')

def get_files(directory):
	files = os.listdir(directory)
	files.sort()
	return files

@app.route('/')
def index():
	url = 'https://theos.kyriasis.com:5000'
	log_dir = '/home/kyrias/znc_logs'

	networks = []
	for network_name in get_files(log_dir):
		network_url = '{}/{}'.format(url, network_name)
		channels = []

		for channel_name in get_files(os.path.join(log_dir, network_name)):
			channel_url  = '{}/{}'.format(network_url, quote_plus(channel_name))
			channel = Channel(channel_name, channel_url, '')
			channels += [channel]

		networks += [Network(network_name, network_url, channels)]
	return(render_template('list_networks.html', networks=networks, url=url))

@app.route('/<network_name>')
def get_network(network_name):
	url = 'https://theos.kyriasis.com:5000'
	network_url = '{}/{}'.format(url, network_name)
	log_dir = '/home/kyrias/znc_logs'

	channels = []
	for channel_name in get_files(os.path.join(log_dir, network_name)):
		channel_url  = '{}/{}'.format(network_url, quote_plus(channel_name))
		channel = Channel(channel_name, channel_url, '')

		channels += [channel]

	network = Network(network_name, network_url, channels)
	return(render_template('show_network.html', network=network, url=url))

@app.route('/<network_name>/<channel_name>')
def channel_logs(network_name, channel_name):
	url = 'https://theos.kyriasis.com:5000'
	network_url = '{}/{}'.format(url, network_name)
	channel_url = '{}/{}'.format(network_url, quote_plus(channel_name))
	log_dir = '/home/kyrias/znc_logs'

	logs = []
	for log_file in get_files(os.path.join(log_dir, network_name, channel_name)):
		log_url = '{}/{}'.format(channel_url, log_file)
		log = Log(log_file, log_url)

		logs += [log]

	channel = Channel(channel_name, channel_url, logs)
	network = Network(network_name, network_url, [channel])
	return(render_template('show_channel.html', network=network, channel=channel, url=url))

@app.route('/<network_name>/<channel_name>/<log_file>')
def get_log(network_name, channel_name, log_file):
	log_dir = '/home/kyrias/znc_logs'
	with open(os.path.join(log_dir, network_name, channel_name, log_file), 'rb') as file:
		log = file.read().decode('utf-8', 'ignore')
	return(render_template('log.html', log=log))

@app.route('/static/<path:filename>')
def send_static(filename):
	return send_from_directory('static', filename)

if __name__ == '__main__':
	app.run(port=7000, debug=True)
#    arguments = docopt(__doc__)
#    main()
