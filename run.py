import os

tree = {}
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

log_dir = 'znc_logs'
networks = os.listdir(log_dir)
networks.sort()

for network in networks:
    html_tree += '<li>' + network
    tree[network] = {}

    channels = os.listdir(os.path.join(log_dir, network))
    channels.sort()

    html_tree += '<ul>'
    for channel in channels:
        html_tree += '<li>' + channel
        tree[network][channel] = []

        dates = os.listdir(os.path.join(log_dir, network, channel))
        dates.sort()

        html_tree += '<ul>'
        for date in dates:
            html_tree += '<li>' + date + '</li>\n'
            tree[network][channel] += [date]
        html_tree += '</ul></li>\n'
        html_tree += '</li>\n'

    html_tree += '</ul></li>\n'

html_tree += '</ul></body></html>'
with open('out.html', 'w') as file:
    file.write(html_tree)
