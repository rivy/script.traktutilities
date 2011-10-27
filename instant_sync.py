# -*- coding: utf-8 -*-
# 

import xbmc,xbmcaddon,xbmcgui
import telnetlib, time

try: import simplejson as json
except ImportError: import json

import threading
from utilities import *
from instant_sync import *

__author__ = "Ralph-Gordon Paul, Adrian Cowan"
__credits__ = ["Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Ralph-Gordon Paul"
__email__ = "ralph-gordon.paul@uni-duesseldorf.de"
__status__ = "Production"

__settings__ = xbmcaddon.Addon( "script.TraktUtilities" )
__language__ = __settings__.getLocalizedString

# Instantly syncronise changes in playcount
def instantSyncPlayCount(data):
    if data['params']['data']['item']['type'] == 'episode':
        info = getEpisodeDetailsFromXbmc(data['params']['data']['item']['id'], ['tvshowid', 'showtitle', 'season', 'episode'])
        if info == None: return
        Debug("[Instant-sync] (episode playcount): "+str(info))
        if data['params']['data']['playcount'] == 0:
            res = setEpisodesUnseenOnTrakt(info['tvshowid'], info['showtitle'], None, [{'season':info['season'], 'episode':info['episode']}])
        elif data['params']['data']['playcount'] == 1:
            res = setEpisodesSeenOnTrakt(info['tvshowid'], info['showtitle'], None, [{'season':info['season'], 'episode':info['episode']}])
        else:
            return
        Debug("[Instant-sync] (episode playcount): responce "+str(res))
    if data['params']['data']['item']['type'] == 'movie':
        info = getMovieDetailsFromXbmc(data['params']['data']['item']['id'], ['imdbnumber', 'title', 'year', 'playcount', 'lastplayed'])
        if info == None: return
        Debug("[Instant-sync] (movie playcount): "+str(info))
        if 'lastplayed' not in info: info['lastplayed'] = None
        if data['params']['data']['playcount'] == 0:
            res = setMoviesUnseenOnTrakt([{'imdb_id':info['imdbnumber'], 'title':info['title'], 'year':info['year'], 'plays':data['params']['data']['playcount'], 'last_played':info['lastplayed']}])
        elif data['params']['data']['playcount'] == 1:
            res = setMoviesSeenOnTrakt([{'imdb_id':info['imdbnumber'], 'title':info['title'], 'year':info['year'], 'plays':data['params']['data']['playcount'], 'last_played':info['lastplayed']}])
        else:
            return
        Debug("[Instant-sync] (movie playcount): responce "+str(res))
        
# Instantly syncronise removal of items from the library
def instantSyncRemove(data):
    if data['params']['data']['type'] == 'episode':
        info = getEpisodeDetailsFromXbmc(data['params']['data']['id'], ['imdbnumber', 'showtitle', 'year', 'season', 'episode'])
        if info == None: return
        Debug("Instant-sync (episode removed): "+str(info))
        res = removeEpisodesFromTraktCollection(info['imdbnumber'], info['showtitle'], info['year'], [{'season':info['season'], 'episode':info['episode']}], daemon=True)
        Debug("Instant-sync (episode removed): responce "+str(res))
        
    if data['params']['data']['type'] == 'movie':
        info = getMovieDetailsFromXbmc(data['params']['data']['id'], ['imdbnumber', 'title', 'year'])
        if info == None: return
        info['imdb_id'] = info['imbdnumber']
        Debug("Instant-sync (movie removed): "+str(info))
        res = removeMoviesFromTraktCollection([info], daemon=True)
        Debug("Instant-sync (movie removed): responce "+str(res))
                
# Instantly syncronise addition of items to the library
def instantSyncAdd(data):
    if data['params']['data']['type'] == 'episode':
        info = getEpisodeDetailsFromXbmc(data['params']['data']['id'], ['imdbnumber', 'showtitle', 'year', 'season', 'episode'])
        if info == None: return
        Debug("Instant-sync (episode added): "+str(info))
        res = addEpisodesToTraktCollection(info['imdbnumber'], info['showtitle'], info['year'], [{'season':info['season'], 'episode':info['episode']}], daemon=True)
        Debug("Instant-sync (episode added): responce "+str(res))
        
    if data['params']['data']['type'] == 'movie':
        info = getMovieDetailsFromXbmc(data['params']['data']['id'], ['imdbnumber', 'title', 'year'])
        if info == None: return
        info['imdb_id'] = info['imbdnumber']
        Debug("Instant-sync (movie added): "+str(info))
        res = addMoviesToTraktCollection([info], daemon=True)
        Debug("Instant-sync (movie added): responce "+str(res))
