#!/usr/bin/env python
from flask import Flask, send_from_directory, render_template
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
html_tree = '''<html><head><style>
.tree, .tree ul{
  font: normal normal 14px/20px Helvetica, Arial, sans-serif;
  list-style-type: none; margin-left: 0 0 0 10px;
  padding: 0; position: relative; overflow:hidden;
}
.tree li{ margin: 0; padding: 0 12px; position: relative; }
.tree li::before, .tree li::after{ content: ''; position: absolute; left: 0; }

/* horizontal line on inner list items */
.tree li::before{ border-top: 1px solid #999; top: 10px; width: 10px; height: 0; }

/* vertical line on list items */
.tree li:after{ border-left: 1px solid #999; height: 100%; width: 0px; top: -10px; }

/* lower line on list items from the first level because they don't have parents */
.tree > li::after{ top: 10px; }

/* hide line from the last of the first level list items */
.tree > li:last-child::after{ display: none; }
.tree ul:last-child li:last-child:after{ height:20px; }
</style></head><body><ul class="tree">'''

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

@app.route('/<network>/<channel>/<log_file>')
def get_log(network, channel, log_file):
	log_dir = '/home/kyrias/znc_logs'
	return send_from_directory(os.path.join(log_dir, network, channel), log_file)

def main():
	print(arguments)
	if arguments['<network>'] and not arguments['<channel>']:
		channels = get_files(os.path.join(log_dir, arguments['<network>']))
		for c in channels:
			print(c)

	elif arguments['<channel>']:
		files = get_files(os.path.join(log_dir, arguments['<network>'], arguments['<channel>']))
		for f in files:
			print(f)

	else:
		networks = get_files(log_dir)
		for n in networks:
			print(n)
			channels = get_files(os.path.join(log_dir, n))
			for c in channels:
				print('\t', c)

if __name__ == '__main__':
	app.run(port=7000, debug=True)
#    arguments = docopt(__doc__)
#    main()
