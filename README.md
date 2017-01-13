# plugin.audio.pocketcasts
Kodi Add-On for PocketCasts.com podcast listening

Status: WIP

# Works...
* Listing My Podcasts
* Listing starred episodes
* Listing episodes in progress
* Listing popular, trending and featured picks
* Listing episode list
* Playing episodes from start
* Starring/Unstarring episodes
* Subscribing/unsubscribing podcasts

# Work in progress...
* Translation
* Documentation
* Resuming podcasts

# Not working
* Everything not available in Pocket Casts web interface (and thus pyhon-pocketcasts module)
* Podcast notes are displayed as comments with ugly HTML formatting, maybe look into html2text python module
* Api authentication is done every addon directory listing. Can it be persisted?
* If the api would provide a method to get an episode by uuid, that would be great
* Starring of unsubscribed podcast episodes does not work, but success is indicated by the API. python-pocketcasts needs to check agains newly-fetched list to ensure success
* Subscribed podcast list should be fetched every plugin-load (costly) or whenever subscribed list needs updating (need to look into caching mechanisms)
