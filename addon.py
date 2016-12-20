# -*- coding: utf-8 -*-
from kodiswift import Plugin
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources',
                'lib', 'python-pocketcasts'))
from pocketcasts import Api

_plugin = Plugin()
_api = Api('tobias.jost@spinweb.de', 'd$QdU!jzG79PSc5c')


def add_fanart(items):
    results = []
    for item in items:
        new_item = item.copy()
        new_item['fanart'] = os.path.join(
                             os.path.dirname(__file__), 'fanart.jpg')
        results.append(new_item)
    return results


def podcasts2items(podcasts):
    items = [{
        'label': podcast.title,
        'path': _plugin.url_for('show_episodes', uuid=podcast.uuid),
        'icon': podcast.thumbnail_url,
        'thumbnail': podcast.thumbnail_url
    } for podcast in podcasts]

    return add_fanart(items)


def episodes2items(episodes):
    items = [{
        'label': episode.title,
        'path': episode.url,
        'icon': episode.podcast.thumbnail_url,
        'thumbnail': episode.podcast.thumbnail_url,
        'is_playable': True
    } for episode in episodes]

    return add_fanart(items)


@_plugin.route('/')
def index():
    items = [
        {
            'label': 'My Podcasts',
            'path': _plugin.url_for('my_podcasts')
        },
        {
            'label': 'New Releases',
            'path': _plugin.url_for('new_episode_released')
        },
        {
            'label': 'In Progress',
            'path': _plugin.url_for('episodes_in_progress')
        },
        {
            'label': 'Starred',
            'path': _plugin.url_for('starred_episodes')
        },
        {
            'label': 'Featured',
            'path': _plugin.url_for('featured_podcasts')
        },
        {
            'label': 'Top Charts',
            'path': _plugin.url_for('popular_podcasts')
        },
        {
            'label': 'Trending Now',
            'path': _plugin.url_for('trending_podcasts')
        },
        {
            'label': 'Search Podcast / Add URL',
            'path': _plugin.url_for('search_podcast')
        }
    ]

    return add_fanart(items)


@_plugin.route('/my_podcasts/')
def my_podcasts():
    return podcasts2items(_api.my_podcasts())


@_plugin.route('/new_episode_released/')
def new_episode_released():
    return episodes2items(_api.new_episodes_released())


@_plugin.route('/episodes_in_progress/')
def episodes_in_progress():
    return episodes2items(_api.episodes_in_progress())


@_plugin.route('/starred_episodes/')
def starred_episodes():
    return episodes2items(_api.starred_episodes())


@_plugin.route('/featured_podcasts/')
def featured_podcasts():
    return podcasts2items(_api.featured_podcasts())


@_plugin.route('/popular_podcasts/')
def popular_podcasts():
    return podcasts2items(_api.popular_podcasts())


@_plugin.route('/trending_podcasts/')
def trending_podcasts():
    return podcasts2items(_api.trending_podcasts())


@_plugin.route('/search_podcast/')
def search_podcast():
    return []  # podcasts2items(_api.popular_podcasts())


@_plugin.route('/podcast/<uuid>/')
def show_episodes(uuid):
    podcast = _api.podcast(uuid)
    return episodes2items(podcast.episodes)


if __name__ == '__main__':
    _plugin.run()
