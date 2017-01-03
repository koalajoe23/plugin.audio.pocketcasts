# -*- coding: utf-8 -*-
import os
import routing
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources',
                'lib', 'python-pocketcasts'))
from pocketcasts import Api

_plugin = routing.Plugin()
_addon = xbmcaddon.Addon()
_api = Api(_addon.getSetting('pocketcasts_email'),
           _addon.getSetting('pocketcasts_password'))
_default_fanart = os.path.join(os.path.dirname(__file__), 'fanart.jpg')


def podcasts2items(podcasts):
    list_items = []
    for podcast in podcasts:
        list_item = xbmcgui.ListItem(podcast.title)
        list_item.setArt({
            'icon': podcast.thumbnail_url,
            'thumb': podcast.thumbnail_url,
            'fanart': _default_fanart
        })
        url = _plugin.url_for(show_episodes, uuid=podcast.uuid)
        list_items.append((url, list_item, True))

    return list_items


def episodes2items(episodes):
    list_items = []
    for episode in episodes:
        podcast = episode.podcast
        list_item = xbmcgui.ListItem(episode.title)
        list_item.setArt({
            'icon': podcast.thumbnail_url,
            'thumb': podcast.thumbnail_url,
            'fanart': _default_fanart
        })
        list_item.setProperty('IsPlayable', 'true')
        url = episode.url
        list_items.append((url, list_item, False))

    return list_items


@_plugin.route('/')
def index():
    items = [
        {
            'label': 'My Podcasts',
            'url': _plugin.url_for(my_podcasts)
        },
        {
            'label': 'New Releases',
            'url': _plugin.url_for(new_episode_released)
        },
        {
            'label': 'In Progress',
            'url': _plugin.url_for(episodes_in_progress)
        },
        {
            'label': 'Starred',
            'url': _plugin.url_for(starred_episodes)
        },
        {
            'label': 'Featured',
            'url': _plugin.url_for(featured_podcasts)
        },
        {
            'label': 'Top Charts',
            'url': _plugin.url_for(popular_podcasts)
        },
        {
            'label': 'Trending Now',
            'url': _plugin.url_for(trending_podcasts)
        },
        {
            'label': 'Search Podcast / Add URL',
            'url': _plugin.url_for(search_podcast)
        }
    ]

    xbmcplugin.setContent(_plugin.handle, 'files')
    list_items = []
    for item in items:
        list_item = xbmcgui.ListItem(item['label'])
        list_item.setArt({
            'fanart': _default_fanart
        })
        list_items.append((item['url'], list_item, True))
    if not xbmcplugin.addDirectoryItems(_plugin.handle, list_items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle)


@_plugin.route('/my_podcasts/')
def my_podcasts():
    items = podcasts2items(_api.my_podcasts())
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/new_episode_released/')
def new_episode_released():
    items = episodes2items(_api.new_episodes_released())
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/episodes_in_progress/')
def episodes_in_progress():
    items = episodes2items(_api.episodes_in_progress())
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/starred_episodes/')
def starred_episodes():
    items = episodes2items(_api.starred_episodes())
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/featured_podcasts/')
def featured_podcasts():
    items = podcasts2items(_api.featured_podcasts())
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/popular_podcasts/')
def popular_podcasts():
    items = podcasts2items(_api.popular_podcasts())
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/trending_podcasts/')
def trending_podcasts():
    items = podcasts2items(_api.trending_podcasts())
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/search_podcast/')
def search_podcast():
    return []  # podcasts2items(_api.popular_podcasts())


@_plugin.route('/podcast/<uuid>/')
def show_episodes(uuid):
    podcast = _api.podcast(uuid)
    items = episodes2items(podcast.episodes)
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)

if __name__ == '__main__':
    _plugin.run()
