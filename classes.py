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
