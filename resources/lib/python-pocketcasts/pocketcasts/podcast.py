# -*- coding: utf-8 -*-
"""TODO 2"""


class Podcast(object):
    class SortOrder(object):
        OldestFirst = 2,
        NewestFirst = 3

    def __init__(self, uuid, api=None, **kwargs):
        self._api = api
        # I don't know what id means, it is an unsigned int or null
        self._uuid = uuid
        self._author = kwargs.pop('author', '')
        self._description = kwargs.pop('description', '')
        self._thumbnail_url = kwargs.pop('thumbnail_url', '')
        self._title = kwargs.pop('title', '')
        self._url = kwargs.pop('url', '')
        self._sort_order = kwargs.pop('sort_order',
                                      Podcast.SortOrder.NewestFirst)
        self._category = kwargs.pop('category', '')
        self._language = kwargs.pop('language', '')

        # I don't know if there are more types than Audio and Video
        # Maybe use an Enum
        self._media_type = kwargs.pop('media_type', 'Unknown')
        self._thumbnail_url_130 = kwargs.pop('thumbnail_url_130', '')
        self._thumbnail_url_280 = kwargs.pop('thumbnail_url_280', '')
        self._thumbnail_url_small = kwargs.pop('thumbnail_url_small', '')

    def __repr__(self):
        return str(self.__dict__)

    @property
    def uuid(self):
        return self._uuid

    @property
    def author(self):
        return self._author

    @property
    def description(self):
        return self._description

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def sort_order(self):
        return self._sort_order

    @property
    def media_type(self):
        return self._media_type

    @property
    def thumbnail_url_130(self):
        return self._thumbnail_url_130

    @property
    def thumbnail_url_280(self):
        return self._thumbnail_url_280

    @property
    def thumbnail_url_small(self):
        return self._thumbnail_url_small

    @classmethod
    def _from_json(cls, json, api=None):
        json = json.copy()
        uuid = json.pop('uuid')
        return cls(uuid, api, **json)

    @property
    def episodes(self):
        return self._api.episodes_for_podcast(self)

    def subscribe(self):
        self._api.subscribe_podcast(self.uuid)

    def unsubscribe(self):
        self._api.unsubscribe_podcast(self.uuid)
