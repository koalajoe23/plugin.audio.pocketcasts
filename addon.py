import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory

plugin = routing.Plugin()

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(all), ListItem("My Podcasts"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/all')
def all():
    endOfDirectory(plugin.handle)

if __name__ == '__main__':
    plugin.run()
