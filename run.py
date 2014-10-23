#!/usr/bin/env python
from flask import Flask, send_from_directory, render_template, url_for
from classes import Network, Channel, Log
from urllib.parse import quote_plus
import sys, os

app = Flask(__name__)
app.config.from_pyfile('application.cfg', silent=True)

app.jinja_env.add_extension('jinja2_highlight.HighlightExtension')
app.jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')

def get_files(directory):
	files = os.listdir(directory)
	files.sort()
	return files

@app.route('/')
def index():
	networks = []
	for network_name in get_files(app.config['ZNC_LOG_DIR']):
		network_url = '{}/{}'.format(app.config['URL'], network_name)
		channels = []

		for channel_name in get_files(os.path.join(app.config['ZNC_LOG_DIR'], network_name)):
			channel_url  = '{}/{}'.format(network_url, quote_plus(channel_name))
			channel = Channel(channel_name, channel_url, '')
			channels += [channel]

		networks += [Network(network_name, network_url, channels)]
	return(render_template('list_networks.html', networks=networks, url=app.config['URL']))

@app.route('/<network_name>')
def get_network(network_name):
	network_url = '{}/{}'.format(app.config['URL'], network_name)

	channels = []
	for channel_name in get_files(os.path.join(app.config['ZNC_LOG_DIR'], network_name)):
		channel_url  = '{}/{}'.format(network_url, quote_plus(channel_name))
		channel = Channel(channel_name, channel_url, '')

		channels += [channel]

	network = Network(network_name, network_url, channels)
	return(render_template('show_network.html', network=network, url=app.config['URL']))

@app.route('/<network_name>/<channel_name>')
def channel_logs(network_name, channel_name):
	network_url = '{}/{}'.format(app.config['URL'], network_name)
	channel_url = '{}/{}'.format(network_url, quote_plus(channel_name))

	logs = []
	for log_file in get_files(os.path.join(app.config['ZNC_LOG_DIR'], network_name, channel_name)):
		log_url = '{}/{}'.format(channel_url, log_file)
		log = Log(log_file, log_url)

		logs += [log]

	channel = Channel(channel_name, channel_url, logs)
	network = Network(network_name, network_url, [channel])
	return(render_template('show_channel.html', network=network, channel=channel, url=app.config['URL']))

@app.route('/<network_name>/<channel_name>/<log_file>')
def get_log(network_name, channel_name, log_file):
	with open(os.path.join(app.config['ZNC_LOG_DIR'], network_name, channel_name, log_file), 'rb') as file:
		log = file.read().decode('utf-8', 'ignore')
	return(render_template('log.html', log=log))

@app.route('/static/<path:filename>')
def send_static(filename):
	return send_from_directory('static', filename)

if __name__ == '__main__':
	app.run(port=7000, debug=True)
#    arguments = docopt(__doc__)
#    main()
