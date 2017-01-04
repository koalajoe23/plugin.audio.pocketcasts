# -*- coding: utf-8 -*-
import os
import requests
import routing
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources',
                'lib', 'python-pocketcasts'))
import pocketcasts

_plugin = routing.Plugin()
_addon = xbmcaddon.Addon()
_api = pocketcasts.Api(_addon.getSetting('pocketcasts_email'),
                       _addon.getSetting('pocketcasts_password'))
_default_fanart = os.path.join(os.path.dirname(__file__), 'fanart.jpg')


def handleException(e):
    if type(e) == requests.exceptions.HTTPError and \
            e.response.status_code == requests.codes.unauthorized:
        xbmcgui.Dialog().ok("Error", "Could not authenticate with "
                            "Pocket Casts.", "Check login credentials!")
        xbmc.log(_addon.getAddonInfo('id'))
        _addon.openSettings()
    else:
        xbmcgui.Dialog().notification('Error occurred', str(e),
                                      xbmcgui.NOTIFICATION_ERROR)


def podcasts2items(podcasts, subscribed_podcast_uuids=None):
    if not subscribed_podcast_uuids:
        try:
            subscribed_podcasts = _api.my_podcasts()
        except requests.exceptions.RequestException as e:
            handleException(e)
            return
        subscribed_podcast_uuids = \
            [podcast.uuid for podcast in subscribed_podcasts]
    list_items = []
    for podcast in podcasts:
        menu_items = []
        podcast_subscribed = (podcast.uuid in subscribed_podcast_uuids)
        list_item = xbmcgui.ListItem(podcast.title)
        if podcast_subscribed:
            menu_items.append(('Unsubscribe', 'XBMC.RunPlugin(' +
                               _plugin.url_for(unsubscribe_podcast,
                                               podcast_uuid=podcast.uuid
                                               ) + ')'))
        else:
            menu_items.append(('Subscribe', 'XBMC.RunPlugin(' +
                               _plugin.url_for(subscribe_podcast,
                                               podcast_uuid=podcast.uuid,
                                               ) + ')'))
        list_item.addContextMenuItems(menu_items)
        list_item.setArt({
            'icon': podcast.thumbnail_url,
            'thumb': podcast.thumbnail_url,
            'fanart': _default_fanart
        })
        list_item.setInfo('music', {
            'album': podcast.title,
            'artist': podcast.author,
            'comment': podcast.description,
            'genre': 'Podcast'
        })
        url = _plugin.url_for(show_episodes, uuid=podcast.uuid)
        list_items.append((url, list_item, True))

    return list_items


def episodes2items(episodes, subscribed_podcast_uuids=None):
    if not subscribed_podcast_uuids:
        try:
            subscribed_podcasts = _api.my_podcasts()
        except requests.exceptions.RequestException as e:
            handleException(e)
            return
        subscribed_podcast_uuids = \
            [podcast.uuid for podcast in subscribed_podcasts]
    list_items = []
    for i, episode in enumerate(episodes):
        podcast = episode.podcast
        label = episode.title
        italics = False
        yellow = False
        menu_items = []
        podcast = episode.podcast
        podcast_subscribed = (episode.podcast.uuid in subscribed_podcast_uuids)
        if episode.starred and podcast_subscribed:
            label = '[S]' + label
            yellow = True
            menu_items.append(('Unstar', 'XBMC.RunPlugin(' +
                               _plugin.url_for(unstar_episode,
                                               podcast_uuid=podcast.uuid,
                                               episode_uuid=episode.uuid,
                                               ) + ')'))
        elif podcast_subscribed:
            menu_items.append(('Star', 'XBMC.RunPlugin(' +
                               _plugin.url_for(star_episode,
                                               podcast_uuid=podcast.uuid,
                                               episode_uuid=episode.uuid,
                                               ) + ')'))
        if episode.played_up_to > 0 and \
                episode.playing_status == \
                pocketcasts.Episode.PlayingStatus.Unplayed:
            m, s = divmod(episode.played_up_to, 60)
            h, m = divmod(m, 60)
            elapsed = '{0:01d}:{1:02d}:{2:02d}'.format(h, m, s)
            label = '[' + elapsed + '] ' + label
            italics = True
        if yellow:
            label = '[COLOR yellow]' + label + '[/COLOR]'
        if italics:
            label = '[I]' + label + '[/I]'
        list_item = xbmcgui.ListItem(label)
        list_item.setArt({
            'icon': podcast.thumbnail_url,
            'thumb': podcast.thumbnail_url,
            'fanart': _default_fanart
        })
        list_item.setInfo('music', {
            'date': episode.published_at.strftime('%d.%m.%Y'),
            'year': episode.published_at.year,
            'album': episode.podcast.title,
            'artist': episode.podcast.author,
            'title': episode.title,
            'tracknumber': len(episodes) - i,
            'comment': episode.notes,
            'duration': episode.duration,
            'genre': 'Podcast'
        })
        list_item.setProperty('IsPlayable', 'true')
        list_item.addContextMenuItems(menu_items)
        url = episode.url
        list_items.append((url, list_item, False))

    return list_items


@_plugin.route('/star_episode/<podcast_uuid>/<episode_uuid>')
def star_episode(podcast_uuid, episode_uuid):
    try:
        _api.mark_as_starred(podcast_uuid, episode_uuid, True)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmc.executebuiltin('Container.Refresh')


@_plugin.route('/unstar_episode/<podcast_uuid>/<episode_uuid>')
def unstar_episode(podcast_uuid, episode_uuid):
    try:
        _api.mark_as_starred(podcast_uuid, episode_uuid, False)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmc.executebuiltin('Container.Refresh')


@_plugin.route('/subscribe_podcast/<podcast_uuid>')
def subscribe_podcast(podcast_uuid):
    try:
        _api.subscribe_podcast(podcast_uuid)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmc.executebuiltin('Container.Refresh')


@_plugin.route('/unsubscribe_podcast/<podcast_uuid>')
def unsubscribe_podcast(podcast_uuid):
    try:
        _api.unsubscribe_podcast(podcast_uuid)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmc.executebuiltin('Container.Refresh')


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


@_plugin.route('/my_podcasts')
def my_podcasts():
    try:
        podcasts = _api.my_podcasts()
        uuids = [podcast.uuid for podcast in podcasts]
        items = podcasts2items(podcasts, subscribed_podcast_uuids=uuids)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/new_episode_released')
def new_episode_released():
    try:
        items = episodes2items(_api.new_episodes_released())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/episodes_in_progress')
def episodes_in_progress():
    try:
        items = episodes2items(_api.episodes_in_progress())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/starred_episodes')
def starred_episodes():
    try:
        items = episodes2items(_api.starred_episodes())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/featured_podcasts')
def featured_podcasts():
    try:
        items = podcasts2items(_api.featured_podcasts())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/popular_podcasts')
def popular_podcasts():
    try:
        items = podcasts2items(_api.popular_podcasts())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/trending_podcasts')
def trending_podcasts():
    try:
        items = podcasts2items(_api.trending_podcasts())
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/search_podcast')
def search_podcast():
    term = xbmcgui.Dialog().input("Enter search term")
    if term:
        _plugin.redirect('/search_podcast/'+term)


@_plugin.route('/search_podcast/<term>')
def search_podcast_results(term):
    try:
        items = podcasts2items(_api.search_podcasts(term))
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    xbmcplugin.setContent(_plugin.handle, 'albums')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)


@_plugin.route('/podcast/<uuid>')
def show_episodes(uuid):
    try:
        podcast = _api.podcast(uuid)
    except requests.exceptions.RequestException as e:
        handleException(e)
        return
    items = episodes2items(podcast.episodes)
    xbmcplugin.setContent(_plugin.handle, 'songs')
    if not xbmcplugin.addDirectoryItems(_plugin.handle, items):
        raise
    xbmcplugin.endOfDirectory(_plugin.handle, cacheToDisc=False)

if __name__ == '__main__':
    _plugin.run()
