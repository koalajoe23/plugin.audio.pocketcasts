==================
python-pocketcasts
==================

python module to interact with the unofficial Pocket Casts API.

**This module is in no way affiliated with or endorsed by shifty jelly! Use at your own risk!**

----

What works
----------
* Receive podcast and episode listings
* Receive episode show notes
* Star and unstar podcast

What is (or at least seems) off limits
--------------------------------------
Everything not doable via web player:

* Next up
* Playlists

I only looked at the web player's api not the android and iOS apps

TODO
----
* API documentation
* docstrings
* Improve error handling
* Packaging as PyPI module

Example
-------
::

  import pocketcasts as pc
  api = pc.Api('user', 'password')::
  
  my_podcasts = api.my_podcasts()           # get my subscribed podcasts
  my_podcast[0].title                       # show first podcasts title
  my_podcasts[2].unsubscribe()              # unsubscribe 3rd podcast
  my_podcast[5].episodes[3].url             # get url of the 4th episode of 6th podcast
  
  cool_podcast = api.popular_podcasts()[0]
  cool_podcast.subscribe()
  cool_podcast.episodes[1].starred = True
  episode = cool_podcast.episodes[0]
  episode.played_up_to = episode.duration / 2 # set the episode exactly half played
  
   
