# -*- coding: utf-8 -*-
"""TODO: Class description API"""
from episode import Episode
from podcast import Podcast
import requests


class Api(object):
    def __init__(self, email, password):
        self._session = requests.Session()
        formdata = {
            "user[email]": email,
            "user[password]": password,
            }
        response = self._session.post("https://play.pocketcasts.com"
                                      "/users/sign_in",
                                      data=formdata)
        response.raise_for_status()
        # TODO(Check if login was successful, code is 200 in every case)

    def my_podcasts(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/all.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def featured_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/featured.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def episodes_for_podcast(self, podcast,
                             sort_order=Podcast.SortOrder.NewestFirst):
        page = 1
        pages_left = True
        episodes = []
        while pages_left:
            params = {'page': page, 'sort': sort_order, 'uuid': podcast.uuid}
            response = self._session.post("https://play.pocketcasts.com"
                                          "/web/episodes/find_by_podcast.json",
                                          json=params)
            response.raise_for_status()

            json_response = response.json()
            for episode_json in json_response['result']['episodes']:
                episode = Episode._from_json(episode_json, podcast)
                # episode = episode_json
                episodes.append(episode)

            # we should never ever receive more episodes than specified
            # well, better be fault tolerant
            if(json_response['result']['total'] > len(episodes)):
                page = page + 1
            else:
                pages_left = False

        return episodes

    def podcast(self, uuid):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/podcast.json",
                                      json={'uuid': uuid})
        response.raise_for_status()
        response_json = response.json()
        podcast = Podcast._from_json(response_json['podcast'], self)

        return podcast

    def popular_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/popular_world.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def trending_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/trending.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def new_episodes_released(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "new_releases_episodes.json")
        response.raise_for_status()

        episodes = []
        podcasts = {}
        for episode_json in response.json()['episodes']:
            podcast_uuid = episode_json['podcast_uuid']
            if podcast_uuid not in podcasts:
                podcasts[podcast_uuid] = self.podcast(podcast_uuid)
            episode = Episode._from_json(episode_json, podcasts[podcast_uuid])
            episodes.append(episode)
        return episodes

    def episodes_in_progress(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "in_progress_episodes.json")
        response.raise_for_status()

        episodes = []
        podcasts = {}
        for episode_json in response.json()['episodes']:
            podcast_uuid = episode_json['podcast_uuid']
            if podcast_uuid not in podcasts:
                podcasts[podcast_uuid] = self.podcast(podcast_uuid)
            episode = Episode._from_json(episode_json, podcasts[podcast_uuid])
            episodes.append(episode)
        return episodes

    def starred_episodes(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "starred_episodes.json")
        response.raise_for_status()

        episodes = []
        podcasts = {}
        for episode_json in response.json()['episodes']:
            podcast_uuid = episode_json['podcast_uuid']
            if podcast_uuid not in podcasts:
                podcasts[podcast_uuid] = self.podcast(podcast_uuid)
            episode = Episode._from_json(episode_json, podcasts[podcast_uuid])
            episodes.append(episode)
        return episodes

    def mark_as_played(self, podcast_uuid, episode_uuid, played):
        playing_status = (Episode.PlayingStatus.Played if played
                          else Episode.PlayingStatus.Unplayed)
        params = {'playing_status': playing_status,
                  'podcast_uuid': podcast_uuid,
                  'uuid': episode_uuid,
                  'played_up_to': 0}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "update_episode_position.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)

    def mark_as_starred(self, podcast_uuid, episode_uuid, starred):
        params = {'starred': starred,
                  'podcast_uuid': podcast_uuid,
                  'uuid': episode_uuid}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "update_episode_star.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)

    def load_notes(self, episode_uuid):
        # Why star/mark played needs podcast uuid and this only episode uuid?
        # ¯\_(ツ)_/¯
        params = {'uuid': episode_uuid}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "show_notes.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)

        show_notes = response.json()['show_notes']

        return show_notes

    def search_podcasts(self, search_string):
        params = {'term': search_string}
        response = self._session.get("https://play.pocketcasts.com"
                                     "/web/podcasts/search.json",
                                     data=params)
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def subscribe_podcast(self, podcast_uuid, subscribe=True):
        if not subscribe:
            return self.unsubscribe(podcast_uuid)

        params = {'uuid': podcast_uuid}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/"
                                      "subscribe.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)

    def unsubscribe_podcast(self, podcast_uuid):
        params = {'uuid': podcast_uuid}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/"
                                      "unsubscribe.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)

    def update_episode_position(self, podcast_uuid, episode_uuid, position,
                                episode_duration=0):
        # TODO(Check position value < duration)
        params = {'playing_status': Episode.PlayingStatus.Unplayed,
                  'podcast_uuid': podcast_uuid,
                  'uuid': episode_uuid,
                  'played_up_to': position,
                  # web player sends duration so do I...
                  'duration': episode_duration}
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "update_episode_position.json",
                                      json=params)
        response.raise_for_status()
        # TODO(Check response for error)
