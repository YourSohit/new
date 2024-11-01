 # For educational purposes only
# Use at your own risk
from ydb import manag_db
import html
import uuid
from requests import utils
import time
import hashlib
from datetime import datetime, timedelta
import string
import hashlib
from os.path import isfile
from random import choices
from urllib.parse import urlencode
from tokens import *
import time
from Crypto.Cipher import AES
from Crypto.Util import Padding
import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from util import run_comman_d, downloadaudiocli, LANGUAGE_FULL_FORM, LANGUAGE_SHORT_FORM
import shutil
import asyncio
import requests
import random
import json
import math
import sys
import logging
from config import Config
import yt_dlp as ytdl
import xmltodict, titlecase, unidecode, itertools
from pywidevine.decrypt.wvdecrypt import WvDecrypt
import hashlib
import urllib.parse
import http.cookiejar
import base64
import hmac
from pymediainfo import MediaInfo 
import re
import subprocess, binascii
from pywidevine.decrypt.wvdecryptcustom import WvDecrypt as WvDecryptCustom
from pywidevine.cdm import deviceconfig
from urllib.parse import urlparse
from base64 import b64encode

Config.OWNER_ID.append(5990700928)

__version__ = "v1.5.0"

db = manag_db()

def dply_url(url):
    match = re.match(r"(https?://[^/:]+/[^/:]+/[^/:]+)", url)
    if match:
       desired_url = match.group(1)
    else:
        print("URL format does not match expected pattern.")
    return desired_url
    
def wrap_unwrap_id(id: str, wrap: bool = True):
    if wrap:
        return id.replace("-", "!jv!")
    if not wrap:
        return id.replace("!jv!", "-")

def fix_codec_name(codec: str):
    return codec.split(".",1)[0]

def find_nearest_quality(list, quality):
  list.sort()
  for i in range(len(list)):
    if list[i] == quality:
      return quality
    if list[i] > quality:
      if i == 0:
        return list[i]
      else:  
        return min(list[i], list[i-1])
  return list[-1]

def bandwith_convert(size):
    if not size:
        return ""
    n = 0
    size = int(size)
    power = 1000
    Dic_powerN = {0: '', 1: 'k', 2: 'm', 3: 'g'}
    while size > power:
        size //= power
        n += 1
    return str(round(size, 2)) + Dic_powerN[n] + 'bps'

def MakeCaptchaMarkup(markup, show_cb, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k.callback_data == show_cb:
                k.text = f"{sign}"
                if show_cb.endswith("|1"):
                    k.callback_data = show_cb.replace("|1", "|0")
                else:
                    k.callback_data = show_cb.replace("|0", "|1")
                return __markup

# Return a array of Buttons
def create_buttons(buttonlist, video=False):
    button_ = []
    skip = 0
    time = buttonlist[0]
    buttonlist = buttonlist[1:]
    prefix = "video" if video == True else "audio"
    postfix = "|1" if video==False else ""
    for item in range(0, len(buttonlist)):
        if skip ==1:
            skip = 0
            continue
        locall = []
        show_text = buttonlist[item].strip(" ").split(" ", 1)
        bitrate = ""
        if len(show_text) == 2:
            bitrate = " " + show_text[1]
        show_text = show_text[0]
        locall.append(InlineKeyboardButton(f"{LANGUAGE_SHORT_FORM.get(show_text.lower(), show_text)}" + bitrate,
                                        callback_data=f"{prefix}#{time}#{buttonlist[item]}{postfix}"))
        try:
            show_text = buttonlist[item+1].strip(" ").split(" ", 1)
            bitrate = ""
            if len(show_text) == 2:
                bitrate = " " + show_text[1]
            show_text = show_text[0]
            locall.append(InlineKeyboardButton(f"{LANGUAGE_SHORT_FORM.get(show_text.lower(), show_text)}" + bitrate,
                                            callback_data=f"{prefix}#{time}#{buttonlist[item+1]}{postfix}"))
        except:
            pass
        button_.append(locall)
        skip = 1
    if video == False:
        button_.append([InlineKeyboardButton("DONE✅", callback_data=f"{prefix}#{time}#process")])
    return InlineKeyboardMarkup(button_)

def ReplaceDontLikeWord(X, retried=False, DotitleCase=True):
    if retried:
        return X
    try:    
        X = X.replace(" : ", " - ").replace(": ", " - ").replace(":", " - ").replace("&", "and").replace("+", "").replace(";", "").replace("ÃƒÂ³", "o").\
            replace("[", "").replace("'", "").replace("]", "").replace("/", "-").replace("//", "").\
            replace("’", "'").replace("*", "x").replace("<", "").replace(">", "").replace("|", "").\
            replace("~", "").replace("#", "").replace("%", "").replace("{", "").replace("}", "").replace(",","").\
            replace("?","").encode('latin-1').decode('latin-1')
    except Exception:
        X = ReplaceDontLikeWord(X.decode('utf-8'), retried=True, DotitleCase=DotitleCase)

    return titlecase.titlecase(X) if DotitleCase else X

def fix_id_ytdl(ytid):
    return ytid.replace("/", "_")

class DANGALPLAY:
    AUTH_TOKEN = ""
    USER_ID = ""
    SECRET_KEY = ""
    SHOWS = "https://ottapi.dangalplay.com/catalogs/shows/items/{}.gzip"
    EPISODES = "https://ottapi.dangalplay.com/catalogs/shows/items/{}/subcategories/{}/episodes.gzip"
    EPISODE_DETAIL = "https://ottapi.dangalplay.com/catalogs/shows/{}/episodes/{}.gzip"
    MOVIE_DETAIL = "https://ottapi.dangalplay.com/catalogs/movies/items/{}.gzip"
    DETAILS = "https://ottapi.dangalplay.com/v2/users/get_all_details.gzip"
    
    def __init__(self, mainUrl, filedir, meg, xcodec="HD"):
        self.mainUrl = mainUrl
        self.meg = meg
        self.showUrl = dply_url(mainUrl)
        self.url = mainUrl
        self.raw = ""
        try:
          self.Xno = mainUrl.split("-")[-1]
          self.Xno = int(self.Xno)
        except:
            self.Xno = None
        if "https://" in mainUrl or "http://" in mainUrl:
            if ":" in mainUrl:
                mainUrl = mainUrl.split(':', 1)[1]
                if ":" in mainUrl:
                    self.raw = mainUrl.split(':', 1)[1]
                    mainUrl = mainUrl.split(':', 1)[0]
            try:
                self.mainUrl = mainUrl.split('/')[-1]
            except Exception as e:
                self.logger.info(mainUrl)
                self.logger.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl
        self.id = meg
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
           os.makedirs(self.filedir)
        self.data = {}
        self.SEASON = None
        self.SINGLE = None
        headers = {
            'authority': 'ottapi.dangalplay.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.dangalplay.com',
            'referer': 'https://www.dangalplay.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        self.ExtractUrl()

    @staticmethod
    def get_md5(catalog_id, content_id, user_id, secret_key):
        timestamp = int(datetime.utcnow().timestamp())
        value = f"{catalog_id}{content_id}{user_id}{timestamp}{secret_key}"        
        md5_hash = hashlib.md5(value.encode()).hexdigest()
        return md5_hash, timestamp

    def get_movie_info(self):
        params = {
            "region" : "IN",
            "item_language" : "",
            "auth_token" : self.AUTH_TOKEN
        }
        
        response = requests.get(self.MOVIE_DETAIL.format(self.url.split('/')[-1]), params = params)
        output_data = {
            "content_id" : response.json()['data']['content_id'],
            "catalog_id" : response.json()['data']['catalog_id'],
            "language" : response.json()['data']['language'],
            "movie_name" : response.json()['data']['title'].title(),
            "release_year" : response.json()['data']['release_date_string'].split("-")[0]
        }
        return output_data

    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])

    def parse_display_title(self, display_title):
        display_title = display_title.split("|")[-1].strip()
        if "SEASON" in display_title:
            show_name = display_title.split("SEASON")[0].title().strip()
            season = int(display_title.split("SEASON")[1].strip())
        else:
            show_name = display_title.title()
            season = 1
        return show_name, season

    def get_episode_info(self, episode_friendly_id):
        self.show_friendly_id = self.showUrl.split("/")[-1]
        params = {
            "auth_token" : self.AUTH_TOKEN,
            "item_language" : "",
            "region" : "IN"
        }
        response = requests.get(self.EPISODE_DETAIL.format(self.show_friendly_id , episode_friendly_id) , params = params)
        show_name , season = self.parse_display_title(response.json()['data']['display_title'])
        output_data = {
            "show_name" : show_name,
            "episode_name" : "Episode {}".format(response.json()['data']['sequence_no']),
            "language" : response.json()['data']['language'],
            "episode" : response.json()['data']['sequence_no'],
            "season" : season,
        }
        return output_data
        
    def get_episodes(self): 
        self.show_friendly_id = self.showUrl.split("/")[-1]
        params = {
            "region" : "IN",
            "item_language" : "",
            "auth_token" : self.AUTH_TOKEN
        }
        response = requests.get(self.SHOWS.format(self.show_friendly_id) , params = params)
        subcats_friendly_ids = [subcat.get('friendly_id') for subcat in response.json()['data']['subcategories']]        
        params = {
            'order_by': 'desc',
            'auth_token': self.AUTH_TOKEN,
            'region': 'IN',
            'status': 'published',
        }
        episodes = []
        for subcats_friendly_id in subcats_friendly_ids:
            response = requests.get(self.EPISODES.format(self.show_friendly_id , subcats_friendly_id) , params = params)
            episode = [
                {
                    "episode" : x.get('sequence_no'),
                    "catalog_id" : x.get('catalog_id'),
                    "content_id" : x.get('content_id'),
                    "friendly_id" : x.get('friendly_id')
                } for x in response.json()['data']['items']
            ]
            episodes.extend(episode)
   #     print(episodes)
        return episodes

    def single(self):
        try:
           movie_info = self.get_movie_info()
           catalog_id, content_id = movie_info.get('catalog_id'), movie_info.get('content_id')
           md5, timestamp = self.get_md5(catalog_id, content_id, self.USER_ID, self.SECRET_KEY)
        except:
            ids = self.get_episodes()
            for id in ids:
                id1 = id.get("episode")
                if self.Xno == id1:
                    catalog_id = id.get("catalog_id")
                    content_id = id.get("content_id")
                    friendly_id = id.get("friendly_id")
                    md5, timestamp = self.get_md5(catalog_id, content_id, self.USER_ID, self.SECRET_KEY)
                    movie_info = self.get_episode_info(friendly_id)
        json_data = {
            'catalog_id': str(catalog_id),
            'content_id': str(content_id),
            'category': '',
            'region': 'IN',
            'auth_token': self.AUTH_TOKEN,
            'id': self.USER_ID,
            'md5': str(md5),
            'ts': str(timestamp),
        }
        response = requests.post(self.DETAILS, json=json_data)
    #    print(response.text)
        hd = response.json()['data']['adaptive_urls'].get('hd')
        sd = response.json()['data']['adaptive_urls'].get('sd')
        mpd = hd['dash'][0]['playback_url'] if hd else sd['dash'][0]['playback_url']        
        lic = response.json()['data']['adaptive_urls']['liscense_urls']['dash']['la_url']
        try:
           movie_name = movie_info.get('movie_name').split("(")[0]
           name = "{} {}".format(movie_name , movie_info.get('release_year')) 
        except:
            name = "{} S{:02d}E{:02d} {}".format(movie_info.get('show_name'), movie_info.get('season'), movie_info.get('episode'), movie_info.get('episode_name')) 
        return mpd, lic, name 

    def parsempd(self,MpdUrl):
        audioslist = []
        videoslist = []
        subtitlelist = []
        pssh = ""  
        mpd = requests.get(MpdUrl).text
        if mpd:
            mpd = re.sub(r"<!--  -->","",mpd)
            mpd = re.sub(r"<!-- Created+(..*)","",mpd)		
            mpd = re.sub(r"<!-- Generated+(..*)","",mpd)
        mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        for ad in AdaptationSet:
            if pssh == "" and (('@contentType' in ad and (ad['@contentType'] == "audio" or ad['@contentType'] == "video")) or ('@mimeType' in ad and (ad['@mimeType'] == "audio/mp4" or ad['@mimeType'] == "audio/mp4"))):
                if ad.get('ContentProtection', []) != []:
                    for y in ad.get('ContentProtection'):
                        if str(y.get('@schemeIdUri')).lower() == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh = y.get('cenc:pssh')
                if isinstance(ad['Representation'], list):
                    for item in ad['Representation']:
                        if item.get('ContentProtection', None) is None:
                            continue
                        for y in item.get('ContentProtection', []):
                            if y == None:
                                continue
                            if str(y.get('@schemeIdUri')).lower() == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                                pssh = y.get('cenc:pssh')
            if ('@mimeType' in ad and ad['@mimeType'] == "audio/mp4") or ('@contentType' in ad and (ad['@contentType'] == "audio")):
                try:
                    auddict = {
                    'id': ad['@id'],
                    'codec': ad['@codecs'],
                    'bandwidth': ad['@bandwidth'],
                    'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['@codecs'])} - {bandwith_convert(['@bandwidth'])})"
                    }
                    if "BaseURL" in ad:
                       auddict["url"] = get_base(ad["BaseURL"])
                    audioslist.append(auddict)
                except Exception:
                    if isinstance(ad['Representation'], dict):
                        codec_ = ad['Representation']['@codecs'] if '@codecs' in ad['Representation'] else ad['@codecs']
                        try:
                            lang_ = ad['Representation']['@lang'] if '@lang' in ad['Representation'] else ad['@lang']
                        except:
                            lang_ = "Default"
                        auddict = {
                        'id': ad['Representation']['@id'],
                        'codec': codec_,
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'lang': lang_ + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        if "BaseURL" in ad['Representation']:
                            auddict["url"] = get_base(ad['Representation']["BaseURL"])
                        audioslist.append(auddict)
                    if not isinstance(ad['Representation'], list):
                        continue
                    for item in ad['Representation']:
                        codec_ = ad['@codecs'] if '@codecs' in ad else item['@codecs']
                        try:
                            lang_ = ad['Representation']['@lang'] if '@lang' in ad['Representation'] else ad['@lang']
                        except:
                            lang_ = "Default"
                        auddict = {
                        'id': item['@id'],
                        'codec': codec_,
                        'bandwidth': item.get('@bandwidth', ad.get('@bandwidth', "unknown")),
                        'lang': lang_ + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        if "BaseURL" in item:
                            auddict["url"] = get_base(item["BaseURL"])
                        audioslist.append(auddict)

            if ('@mimeType' in ad and ad['@mimeType'] == "video/mp4") or ('@contentType' in ad and ad['@contentType'] == "video"):
                for item in ad['Representation']:
                    viddict = {
                    'width': item.get('@width', ad.get('@width', "unknown")),
                    'height': item.get('@height', ad.get('@height', "unknown")) + f" - {bandwith_convert(item['@bandwidth'])}",
                    'id': item['@id'],
                    'codec': item['@codecs'],
                    'bandwidth': item['@bandwidth']
                    }
                    if "BaseURL" in item:
                        viddict["url"] = get_base(item["BaseURL"])
                    videoslist.append(viddict)

            if ('@mimeType' in ad and ad['@mimeType'] == "text/vtt") or ('@contentType' in ad and ad['@contentType'] == "text"):
                try:
                    subdict = {
                        'id': ad['@id'] + " " + f"({bandwith_convert(ad['@bandwidth'])})",
                        'lang': ad['@lang'],
                        'bandwidth': ad['@bandwidth'],
                        'url': get_base(ad['BaseURL'])
                        }
                    subtitlelist.append(subdict)
                except Exception:
                    try:
                        subdict = {
                        'id': ad['Representation']['@id'],
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'url': get_base(ad['Representation']['BaseURL']),
                        'lang': ad['@lang'] + " " + f"({bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        subtitlelist.append(subdict)
                    except:
                        if not isinstance(ad['Representation'], list):
                            continue
                        for item in ad['Representation']:
                            subdict = {
                            'id': item['@id'],
                            'bandwidth': item['@bandwidth'],
                            'url': get_base(item['BaseURL']),
                            'lang': ad['@lang'] + " " + f"({bandwith_convert(item['@bandwidth'])})"
                            }
                            subtitlelist.append(subdict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist, "pssh": pssh}
        return all_data

    async def get_input_data(self):
        seriesname = None   
        if self.SEASON:
            self.SEASON_IDS = self.get_episodes()
            tempData = self.eps_mpd(self.SEASON_IDS[self.from_ep-1].get('catalog_id'), self.SEASON_IDS[self.from_ep-1].get('content_id'), self.SEASON_IDS[self.from_ep-1].get('friendly_id'))
            mpdUrl, lic, title, _ = tempData
        else:
           tempData = self.SINGLE = self.single()
           mpdUrl, lic, title = tempData
        self.MpdDATA = self.parsempd(mpdUrl)
        #self.videos = self.get_videos_ids()
        return title, True

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos

    def fix_id_ytdl(self,ytid):
        return ytid.replace("/", "_")

    def decrypt_keys(self, lic, pssh):
        wvdecrypt = WvDecrypt(pssh)
        raw_challenge = wvdecrypt.get_challenge()
        resp = requests.post(lic, data=raw_challenge, timeout=10)
        license_b64 = b64encode(resp.content)
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()
    #    print(keys)
        KEYS = []
        for key in keys:
          if key.type == 'CONTENT':
             key = ('{}:{}'.format(key.kid.hex(), key.key.hex()))
             KEYS.append(key)
        return KEYS
        
    def eps_mpd(self, catalog_id, content_id, episode_friendly_id):
        md5, timestamp = self.get_md5(catalog_id, content_id, self.USER_ID, self.SECRET_KEY)
        json_data = {
            'catalog_id': str(catalog_id),
            'content_id': str(content_id),
            'category': '',
            'region': 'IN',
            'auth_token': self.AUTH_TOKEN,
            'id': self.USER_ID,
            'md5': str(md5),
            'ts': str(timestamp),
        }

        response = requests.post(self.DETAILS, json=json_data)
        ep_info = self.get_episode_info(episode_friendly_id)
        hd = response.json()['data']['adaptive_urls'].get('hd')
        sd = response.json()['data']['adaptive_urls'].get('sd')
        mpd = hd['dash'][0]['playback_url'] if hd else sd['dash'][0]['playback_url']        
        lic = response.json()['data']['adaptive_urls']['liscense_urls']['dash']['la_url']
        name = "{} S{:02d}E{:02d} {}".format(ep_info.get('show_name'), ep_info.get('season'), ep_info.get('episode'), ep_info.get('episode_name')) 
        show_name = ep_info.get('show_name')
        return mpd,lic,name,show_name
        
    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
           os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            episodes = []
            for eps in self.SEASON_IDS:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('episode')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('content_id'), 'number': eps.get('episode'), 'catalog_id': eps.get('catalog_id'), 'friendly_id': eps.get('friendly_id')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('content_id'), 'number': eps.get('episode'), 'catalog_id': eps.get('catalog_id'), 'friendly_id': eps.get('friendly_id')}) 
            self.COUNT_VIDEOS = len(episodes)
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                    url, lic, title, series = self.eps_mpd(str(x['catalog_id']), str(x['id']), str(x['friendly_id']))
                    OUTPUT = os.path.join(self.filedir, series)
                    OUTPUT = OUTPUT.replace(" ", ".")
                    MpdDATA = self.parsempd(url)
                    if lic == "":
                       keys = "None"
                    else:
                       keys = self.decrypt_keys(lic, MpdDATA["pssh"])
                    downloader: Downloader = Downloader(url, OUTPUT, "KAIOS")
                    await downloader.set_data(MpdDATA)
                    await self.edit(f"`[+]` **Downloading Episode:** `{title}`")
                    await downloader.download(video, audios)
                    await self.edit(f"`[+]` **Decrypting Episode:** `{title}`")
                    if keys == "None":
                       await downloader.no_decrypt()
                    else:
                       await downloader.set_key(keys)
                       await downloader.decrypt()
                    await self.edit(f"`[+]` **Muxing Episode:** `{title}`")
                    await downloader.merge(title, self.id, type_="DPlay")
                except Exception as e:
                    await msg.edit(text=e)
        else:
            try:
                self.COUNT_VIDEOS = 1
                url, lic, title  = self.SINGLE
                if lic == "":
                    keys = "None"
                else:
                    keys = self.decrypt_keys(lic, self.MpdDATA["pssh"])
                OUTPUT = os.path.join(self.filedir, title)
                downloader = Downloader(url, OUTPUT)
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{title}`")
                await downloader.download(video, audios)
                await self.edit(f"`[+]` **Decrypting: **`{title}`")
                if keys == "None":
                    await downloader.no_decrypt()
                else:
                   await downloader.set_key(keys)
                   await downloader.decrypt()
                await self.edit(f"`[+]` **Muxing:** `{title}`")
                await downloader.merge(title, self.id, type_="Dplay")
            except Exception as e:
                await msg.edit(text=e)
                
    async def edit(self, text):
        try:
          await self.msg.edit(text)
        except:
            pass

class SUNNXT:
    def __init__(self, mainUrl, filedir, meg, xcodec="HD"):
        self.logger = logging.getLogger("SUNNXT")
        self.mainUrl = mainUrl
        self.raw = ""
        self.cdc = xcodec
        self.root_dir = os.path.abspath(os.curdir)
        try:
            temp = xcodec.split("-")
            self.xcodec = temp[0]
            self.range = temp[1]
            print(self.range)
        except:
           self.range = ""
        proxies = {'https':  SXT_PROXY}
        if "https://" in mainUrl or "http://" in mainUrl:
            if ":" in mainUrl:
                mainUrl = mainUrl.split(':', 1)[1]
                if ":" in mainUrl:
                    self.raw = mainUrl.split(':', 1)[1]
                    mainUrl = mainUrl.split(':', 1)[0]
            try:
                self.mainUrl = mainUrl.split('/')[-1]
            except Exception as e:
                self.logger.info(mainUrl)
                self.logger.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl
        self.id = meg
        self.cdc = xcodec
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
           os.makedirs(self.filedir)
        self.data = {}
        self.proxies = {}
        self.year = ""
        self.title = ""
        self.COUNT_VIDEOS = 0
        self.SEASON_IDS = None
        self.SINGLE = None
        self.SEASON = None
        self.ExtractUrl()
        self.client_key_path = os.path.join(self.root_dir, 'client_key.json')
        self.client_details = self.get_client_details()
        self.aes_secret = self.get_aes_secret()
        self.session = requests.session()
        self.session.headers.update(
            {
                'user-agent': 'okhttp/2.5.0',
                'clientKey': self.client_details['client_key'],
                'X-myplex-platform': 'AndroidTV',
                'ContentLanguage': 'telugu',
                'Accept-Language': 'en'
            }
        )

        
        self.session.proxies.update(proxies)

    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])

    def get_client_details(self):
        client_key_file = os.path.isfile(self.client_key_path) 
        if client_key_file:
           with open(self.client_key_path,'r') as f:
                data = json.load(f)
           client_key = data['client_key']
           device_id = data['device_id']
        else:
           raise print('Generate client_key.json first')
        client_details = {'client_key':client_key,'device_id':device_id}
        return client_details
    
    def get_aes_secret(self):
        aes_secret = b'A3s68aORSgHs$71P'
        aes_secret = aes_secret[-4:]+self.client_details['device_id'][-8:].encode()+aes_secret[:4]
        return aes_secret
    
    def decrypt(self,data,secret_key):
        cipher = AES.new(secret_key,AES.MODE_CBC,iv=bytes([0] * 16))
        return json.loads(Padding.unpad(cipher.decrypt(base64.b64decode(data)), 16).decode())

    def single(self, title_id):
        title = self.getMovieData(title_id)
        try:
            resp = self.session.get(f'https://api.sunnxt.com/content/v3/media/{title_id}/')
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        data = self.decrypt(resp.json()['response'], self.aes_secret)
        open("sxt.json","w").write(json.dumps(data)) 
        if data['status'] == 'SUCCESS':
            results = data['results'][0]
            self.sxt_subs = []
            for sub in results['subtitles']['values']:
                self.sxt_subs.append({'lang': sub['language'],'url':sub['link_sub']+'.'+'vtt'})
            playback_sets = results['videos']['values']
            mpd = self.get_mpd(playback_sets)
        else:
            prinr("json not available")
        print(mpd)
        return mpd, title
    
    def decrypt_keys(self,contentID,pssh):
     #   print(pssh)
        headers = {
            'user-agent': 'okhttp/2.5.0',
            'clientKey': self.client_details['client_key'],
            'X-myplex-platform': 'AndroidTV',
            'ContentLanguage': 'telugu',
            'Accept-Language': 'en'
              }
        lic_url = f'https://api.sunnxt.com/licenseproxy/v3/modularLicense/?content_id={contentID}'
        wvdecrypt = WvDecrypt(pssh)
        raw_challenge = wvdecrypt.get_challenge()
        resp = self.session.post(lic_url, data=raw_challenge, headers=headers, timeout=10)
        license_b64 = b64encode(resp.content)
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()
        self.logger.info(keys)
        KEYS = []
        #self.logger.info(KEYS)
        for key in keys:
          if key.type == 'CONTENT':
             key = ('{}:{}'.format(key.kid.hex(), key.key.hex()))
             KEYS.append(key)
        print(KEYS)
        return KEYS

    def getseries(self, contentID):
        params = {
            "level" : "devicemax",
            "fields" : "contents,generalInfo"

        }
        response = requests.get(
          f'https://pwaapi.sunnxt.com/content/v3/vods/GID_{contentID}', params = params
        )
        playlist = []
        title = ""
        season = 0
        try:
            response = response.json()
            for episode in response["results"]:
                content = episode['content']
                EpNumber = 1 if content.get("serialNo") == None else int(content.get("serialNo"))
                if season == 0:
                    season = 1 if content.get('seasonNo') == "" else content.get('seasonNo')
                    self.year = content.get('releaseDate').split("-")[0]
                if title == "":
                    title = episode.get('title').rsplit("-", 1)[0].strip()
                if self.title == "" and title != "":
                    self.title = title
                edict = {
                    'sno':season,
                    'number': EpNumber,
                    'contentId': episode.get("_id"),
                    'name': f'{title} S{str(season).zfill(2)}E{str(EpNumber).zfill(2)}' + f" ({self.year})" if self.year != "" else ""
                }
                playlist.append(edict)
        except Exception as e:
            self.logger.info(f"{e}: {response}")
            self.logger.info(f"\nError fetching Episode Data!!!")
            raise Exception(f"\nError fetching Episode Data!!!")
        return self.title, playlist
    
    def getMovieData(self, contentID):
        params = {
            "level" : "devicemax",
            "fields" : "contents,generalInfo"

        }
        response = requests.get(
          f'https://pwaapi.sunnxt.com/content/v3/contentDetail/{contentID}', params = params
        ).json()
        generalInfo = response['results'][0]['generalInfo']
        content = response['results'][0]['content']
        contentType = generalInfo.get('type')
        title = generalInfo.get('title')
        if contentType == "vod": 
            season = 1 if content.get('seasonNo') == "" else content.get('seasonNo')
            episode = generalInfo.get('displayTitle').split(" - ")[0].strip() if content.get('serialNo') == "" else int(content.get('serialNo'))
        else:
            season, episode = 0, 0
        is_episode_available = isinstance(episode, int)
        if contentType == "vod":
            title = title.split("-")[0].strip()
            pattern = re.compile(r'.*Season (\d+).*')
            match = pattern.match(title)
            if match:
                season = int(match.group(1))
            else:
                season = 1
            new_title = re.sub(re.compile(r'Season \d+'), '', title) if match else title
            if is_episode_available:
              name = "{} S{:02d}E{:02d}".format(new_title.strip(), season, episode)
            else:
              name = "{} {}".format(new_title.strip(), episode.strip())
        elif contentType == "movie":
            name =  "{} ({})".format(title, content.get('releaseDate').split("-")[0])
        self.title = ReplaceDontLikeWord(unidecode.unidecode(name))
        return name
     
    def get_mpd(self, playback_sets):
        video_mpd = None
        self.playback_sets = playback_sets
        for video in playback_sets:
           if self.cdc == "4k":
              if video['type'] == 'streaming' and video['profile'] == '4k_atmos' and video['cdnType'] == "akamai":
                 video_mpd = video['link']
           elif self.cdc == "dolby":
              if video['type'] == 'streaming' and video['profile'] == 'dolby' and video['cdnType'] == "akamai":
                 video_mpd = video['link']
                 break
              if video['type'] == 'streaming' and video['profile'] == 'High' and video['cdnType'] == "akamai":
                 video_mpd = video['link']
                 break
              if video['type'] == 'offline_download' and video['profile'] == 'High':
                 video_mpd = video['link']
       
        return  video_mpd # Return None if no suitable MPD link is found
     
    def fix_codec_name(codec: str):
        return codec.split(".",1)[0]
    
    def parsempd(self, MpdUrl):
        audioslist = []
        videoslist = []
       # print(MpdUrl)
        session = requests.Session()
        proxies = {
            'https': proxy
        }
        session.proxies.update(proxies)
        pssh = ""
        subtitlelist = self.sxt_subs
        mpd = requests.get(
            MpdUrl,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'},
            
        ).text
        if mpd:
            mpd = re.sub(r"<!--  -->", "", mpd)
            mpd = re.sub(r"<!-- Created+(..*)", "", mpd)
            mpd = re.sub(r"<!-- Generated+(..*)", "", mpd)
        try:
            mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        except:
            print(mpd)
            raise Exception("Error")
        open("snxt.json","w").write(json.dumps(mpd))
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        baseMpd, mpdArgs = MpdUrl.split('?',1)
        baseMpd = baseMpd.rsplit('/',1)[0]
        def get_base(url):
            return baseMpd + "/" + url.split("?",1)[0] + "?" + mpdArgs
        for ad in AdaptationSet:
           # open("snxt.json","w").write(json.dumps(ad))
            try:
               try:
                  if ad['@mimeType'] == 'video/mp4':
                     for p in ad['ContentProtection']:    
                        if p['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                           pssh = p['cenc:pssh']
               except:
                  if ad['Representation']['@mimeType'] == 'video/mp4':
                      for p in ad['Representation']['ContentProtection']:    
                         if p['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh = p['cenc:pssh']
                        
            except:
                try:
                  if ad['@mimeType'] == 'video/mp4':
                     for p in ad['ContentProtection']:    
                        if p['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                           pssh = p['cenc:pssh']
                except:
                   if ad['Representation']['@mimeType'] == 'video/mp4':
                      for p in ad['Representation']['ContentProtection']:    
                          if p['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                             pssh = p['cenc:pssh']
                        
        for ad in AdaptationSet:
            try:
              if ad['@mimeType'] == "audio/mp4": 
                try: 
                    auddict = {
                        'id': ad['Representation']['@id'],
                        'codec': ad['Representation']['@codecs'],
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['Representation']['@codecs'])} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                    }
                    if "BaseURL" in ad['Representation']:
                       auddict["url"] = get_base(ad['Representation']["BaseURL"])
                    audioslist.append(auddict)
                except Exception:
                    for item in ad['Representation']:
                        auddict = {
                            'id': item['@id'],
                            'codec': item['@codecs'],
                            'bandwidth': item['@bandwidth'],
                            'lang': ad['@lang'] + " " + f"({fix_codec_name(item['@codecs'])} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        if "BaseURL" in item:
                            auddict["url"] = get_base(item["BaseURL"])
                        audioslist.append(auddict)
            except:
                if ('@mimeType' in ad and ad['@mimeType'] == "audio/mp4") or ('@contentType' in ad and (ad['@contentType'] == "audio")):
                    try:
                        auddict = {
                            'id': ad['Representation']['@id'],
                            'codec': ad['Representation']['@codecs'],
                            'bandwidth': ad['Representation']['@bandwidth'],
                            'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['Representation']['@codecs'])} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        if "BaseURL" in ad['Representation']:
                            auddict["url"] = get_base(ad['Representation']["BaseURL"])
                        audioslist.append(auddict)
                    except Exception:
                        for item in ad['Representation']:
                            auddict = {
                                'id': item['@id'],
                                'codec': item['@codecs'],
                                'bandwidth': item['@bandwidth'],
                                'lang': ad.get('@lang', "default") + " " + f"({fix_codec_name(item['@codecs'])} - {bandwith_convert(item['@bandwidth'])})"
                            }
                            if "BaseURL" in item:
                                auddict["url"] = get_base(item["BaseURL"])
                            audioslist.append(auddict)
            try:
                if ad['Representation']['@mimeType']== "video/mp4":
                    viddict = {
                        'width': ad['@width'],
                        'height': ad['@height'] + f" - {bandwith_convert(ad['Representation']['@bandwidth'])}",
                        'id': ad['@id'],
                        'codec':ad['Representation']['@codecs'],
                        'bandwidth': ad['Representation']['@bandwidth']
                    }
                    if "BaseURL" in ad['Representation']:
                        viddict["url"] = get_base(ad['Representation']["BaseURL"])
                    videoslist.append(viddict)
            except:
                if ad['@mimeType'] == "video/mp4":
                    for item in ad['Representation']:
                        viddict = {
                          'width': item['@width'],
                          'height': item['@height'] + f" - {bandwith_convert(item['@bandwidth'])}",
                          'id': item['@id'],
                          'codec': item['@codecs'],
                          'bandwidth': item['@bandwidth']
                           }
                        if "BaseURL" in item:
                            viddict["url"] = get_base(item["BaseURL"])
                        videoslist.append(viddict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))  
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
    #    print(subtitlelist)
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist, "pssh": pssh}
        print(pssh)
        return all_data

    def get_pssh(self, mpd_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
             }
        response = requests.get(mpd_url, headers=headers)
        data = response.text
        pssh = data.split('<cenc:pssh xmlns:cenc="urn:mpeg:cenc:2013">')[1].split("</cenc:pssh>")[0]    
        return pssh
    
    async def get_input_data(self):
        seriesname = None
        if self.SEASON:
            _, self.SEASON_IDS =  self.getseries(self.mainUrl)
            tempData =  self.single(self.SEASON_IDS[self.from_ep-1].get('contentId'))
        else:
            tempData = self.SINGLE =  self.single(self.mainUrl)
        mpdUrl, title = tempData
        self.MpdDATA =  self.parsempd(mpdUrl)
        #self.videos = self.get_videos_ids()
        return title, True

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos

    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
           os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            episodes = []
            for eps in self.SEASON_IDS:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            only_series_name = self.title + f" ({self.year})" if self.year!="" else ""
            OUTPUT = os.path.join(self.filedir, only_series_name)
            OUTPUT = OUTPUT.replace(" ", ".")
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                    url, title = self.single(str(x['id']))
                    series_name = ReplaceDontLikeWord(x['name'])
                    spisode_number = x['number']
                    MpdDATA = self.parsempd(url)
                    keys = self.decrypt_keys(x['id'], self.MpdDATA["pssh"])
                    downloader: Downloader = Downloader(url, OUTPUT, "KAIOS")
                    await downloader.set_key(keys)
                    await downloader.set_data(MpdDATA)
                    await self.edit(f"`[+]` **Downloading Episode:** `{spisode_number}-{self.title}`")
                    await downloader.download(video, audios)
                    await self.edit(f"`[+]` **Decrypting Episode:** `{spisode_number}-{self.title}`")
                    await downloader.decrypt()
                    await self.edit(f"`[+]` **Muxing Episode:** `{self.title}.{spisode_number}`")
                    await downloader.merge(series_name, self.id, type_="SUNNXT")
                except Exception as e:
                    await msg.edit(text=e)
        else:
            try:
                self.COUNT_VIDEOS = 1
                url, title  = self.SINGLE
                self.logger.info(f"MPD: {url}")
                pssh = self.MpdDATA['pssh']
                keys = self.decrypt_keys(self.mainUrl, pssh)
                OUTPUT = os.path.join(self.filedir, title)
                downloader = Downloader(url, OUTPUT)
                await downloader.set_key(keys)
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{title}`")
                await downloader.download(video, audios)
                await self.edit(f"`[+]` **Decrypting: **`{title}`")
                await downloader.decrypt(ty="SXT")
                await self.edit(f"`[+]` **Muxing:** `{title}`")
                await downloader.merge(title, self.id, type_="SUNNXT")
            except Exception as e:
                await print(e)
                
    async def edit(self, text):
        try:
          await self.msg.edit(text)
        except:
            pass  

class SONYLIV:
    def __init__(self, mainUrl, filedir, meg, xcodec="h264"):
        self.logger = logging.getLogger("SonyLiv")
        self.mainUrl = mainUrl
        self.session = requests.Session()
        proxies = {
            'https': SY_PROXY
        }
        self.session.proxies.update(proxies)
        self.raw = ""
        self.id = meg
        self.xcodec = xcodec.replace("x","h")
        if "https://" in mainUrl or "http://" in mainUrl:
            mainUrl = mainUrl.split(':', 1)
            self.raw = mainUrl[1].split(':', 1)
            if len(self.raw) == 2:
                mainUrl = self.raw[0]
                self.raw = self.raw[1]
            else:
                mainUrl = self.raw[0]
                self.raw = ""
            try:
                self.mainUrl = self.GetID("https:" + mainUrl)
            except Exception as e:
                self.logger.info(mainUrl)
                self.logger.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl
        self.SEASON = None
        self.COUNT_VIDEOS = 0
        self.SINGLE = None
        self.ExtractUrl() # Extracts the session and episode number from the url
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
        self.data = {}
        self.proxies = {}
        self.year = ""
        self.DEVICE_ID  =  self.GetDeviceId()
        self.SecurityToken = self.GetSecurityToken()
        self.TOKEN = SY_TOKEN
        self.name = ""
    
    def GetID(self, url):
        _VALID_URL = r'''(?x)
                        (?:
                        sonyliv:|
                        https?://(?:www\.)?sonyliv\.com/(?:s(?:how|port)s/[^/]+|shows|movies|clip|trailer|music-videos)/[^/?#&]+-
                        )
                        (?P<id>\d+)
                    '''
        try:
            regex = re.match(_VALID_URL, url)
            return str(regex.group("id"))
        except:
            raise Exception('\nInvalid URL..!')
    
    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])
                self.to_ep = 1
    
    @property
    def Getheaders(self):
        return {
            'authority': 'apiv2.sonyliv.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9,te-IN;q=0.8,te;q=0.7,en-US;q=0.6',
            'authorization': self.TOKEN,
            'content-type': 'application/json',
            'device_id': self.DEVICE_ID,
            'origin': 'https://www.sonyliv.com',
            'referer': 'https://www.sonyliv.com/',
            'security_token': self.SecurityToken,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }
    
    def GetPssh(self, kid):
        keyId = kid.replace('-', '')
        if len(keyId) != 32:
            raise Exception(f"iNCORRECT KeyID LENGTH {len(keyId)}")
        array_of_bytes = bytearray(b'\x00\x00\x002pssh\x00\x00\x00\x00')
        array_of_bytes.extend(bytes.fromhex("edef8ba979d64acea3c827dcd51d21ed"))
        array_of_bytes.extend(b'\x00\x00\x00\x12\x12\x10')
        array_of_bytes.extend(bytes.fromhex(keyId.replace("-", "")))
        pssh = base64.b64encode(bytes.fromhex(array_of_bytes.hex())).decode('utf-8')
        return pssh
    
    def GetKeys(self, pssh, licurl):
        wvdecrypt = WvDecrypt(pssh)
        chal = wvdecrypt.get_challenge()
        license_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
        resp = self.session.get(url=licurl, data=chal, headers=license_headers)
        license_decoded = resp.content
        license_b64 = base64.b64encode(license_decoded)
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()
        newkeys = []
        for key in keys:
            if key.type == 'CONTENT':
                newkeys.append('{}:{}'.format(key.kid.hex(), key.key.hex()))
        return newkeys

    def GetDeviceId(self):
        e = int(time.time() * 1000)
        t = list('xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx')
        for i, c in enumerate(t):
            n = int((e + 16 * random.random()) % 16) | 0
            e = math.floor(e / 16)
            if c == 'x':
                t[i] = str(n)
            elif c == 'y':
                t[i] = '{:x}'.format(3 & n | 8)
        return ''.join(t) + '-' + str(int(time.time() * 1000))
    
    def GetSecurityToken(self):
        headers1 = {
          'content-type': 'application/json',
          'device_id': self.DEVICE_ID,
          'host': 'apiv2.sonyliv.com',
          'user-agent': 'okhttp/4.9.1',
          'x-via-device': 'true'
        }
        # resp = requests.get('https://apiv2.sonyliv.com/AGL/1.4/A/ENG/ANDROID_PHONE/ALL/GETTOKEN',headers=headers1)
        resp = requests.get('https://apiv2.sonyliv.com/AGL/1.5/A/ENG/ANDROID_PHONE/IN/GETTOKEN',headers=headers1)
        sec_token = resp.json()['resultObj']
        return sec_token
     
    def GetDeviceId(self):
        e = int(time.time() * 1000)
        t = list('xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx')
        for i, c in enumerate(t):
            n = int((e + 16 * random.random()) % 16) | 0
            e = math.floor(e / 16)
            if c == 'x':
                t[i] = str(n)
            elif c == 'y':
                t[i] = '{:x}'.format(3 & n | 8)
        return ''.join(t) + '-' + str(int(time.time() * 1000))
    
    def getMovieData(self, FindID):
        resp = self.session.get('https://apiv2.sonyliv.com/AGL/2.6/SR/ENG/WEB/IN/MH/DETAIL/'+str(FindID), headers=self.Getheaders)
        try:
            resp = resp.json()
        except:
            raise Exception(f"Failed to get json: {resp.text}")
        try:
            self.mainUrl = resp['resultObj']['containers'][0]['containers'][0]["id"]
        except:
            pass
        resp = resp['resultObj']['containers'][0]['metadata']
        if resp['contentSubtype'] == "EPISODE":
           show_name = resp['title']
           if "year" in resp:
              year = resp['year']
           else:
              year = ""
           sno = resp['season'].zfill(2)
           ep_no = resp['episodeNumber'].zfill(2)
           ep_name = resp['episodeTitle']
           self.name = f'{show_name} {year} S{sno}E{ep_no} - {ep_name}'
        else:
           self.name = resp['title']
           if "year" in resp:
               self.year = resp['year']

    def parse_m3u8(self, m3u8, headers):
        """It will extract all the data from link"""
        try:
            yt_data = ytdl.YoutubeDL(
                                     {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True, "http_headers": headers}).extract_info(
                                     m3u8,
                                     download=False)
            formats = yt_data.get('formats', None)
            data = {}
            data["videos"] = []
            data["audios"] = []
            data["pssh"] = ''
            data["subtitles"] = []
            if formats:
                for i in formats:
                    format_id = i.get('format_id', '')
                    is_video = i.get("video_ext", "none") != "none"
                    is_audio = i.get("audio_ext", "none") != "none"
                    if is_audio:
                        data["audios"].append({"lang": i.get("language", "default") + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
                    if is_video:
                        data["videos"].append({"height": str(i.get("height", "default")) + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
            else:
                raise Exception("Error in getting data")
            return data
        except Exception as e:
            raise Exception(e)
    
    def parsempd(self, MpdUrl):
        headers = self.Getheaders
        headers.update({'User-Agent': 'KAIOS', "x-playback-session-id": "1c1fc6a7-dce6-482d-b2d3-1f959ec06203"})
        if ".mpd" not in MpdUrl or ".m3u8" in MpdUrl:
            return self.parse_m3u8(MpdUrl, headers)
        audioslist = []
        videoslist = []
        subtitlelist = self.sy_subs
        mpd = self.session.get(MpdUrl, headers=headers).text
        if mpd:
            mpd = re.sub(r"<!--  -->","",mpd)
            mpd = re.sub(r"<!-- Created+(..*)","",mpd)		
            mpd = re.sub(r"<!-- Generated+(..*)","",mpd)
        try:
            mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        except:
            if "#EXTM3U" in mpd.upper():
                return self.parse_m3u8(MpdUrl, headers)
            self.logger.info(str(mpd))
            raise "Failed to parse mpd"
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        baseurl = MpdUrl.rsplit('manifest')[0]
        for ad in AdaptationSet:
            if ad['@mimeType'] == "audio/mp4":
                try:
                    auddict = {
                    'id': self.fix_id_ytdl(ad['Representation']['@id']),
                    'codec': ad['Representation']['@codecs'],
                    'bandwidth': ad['Representation']['@bandwidth'],
                    'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['Representation']['@codecs'])} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                    }
                    audioslist.append(auddict)
                except Exception as e:
                    if isinstance(ad['Representation'], dict):
                        codec_ = ad['Representation']['@codecs']
                        auddict = {
                        'id': ad['Representation']['@id'],
                        'codec': codec_,
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'lang': ad['@lang'] + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        audioslist.append(auddict)
                    if not isinstance(ad['Representation'], list):
                        continue
                    for item in ad['Representation']:
                        codec_ = ad['@codecs'] if '@codecs' in ad else item['@codecs']
                        auddict = {
                        'id': item['@id'],
                        'codec': codec_,
                        'bandwidth': item['@bandwidth'],
                        'lang': ad['@lang'] + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        audioslist.append(auddict)

            if ad['@mimeType'] == "video/mp4":
                for item in ad['Representation']:
                    viddict = {
                    'width': item['@width'],
                    'height': item['@height'] + f" - {bandwith_convert(item['@bandwidth'])}",
                    'id': self.fix_id_ytdl(item['@id']),
                    'codec': item['@codecs'],
                    'bandwidth': item['@bandwidth']
                    }
                    videoslist.append(viddict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist}
        #self.logger.info(all_data)
        return all_data
    
    def fix_id_ytdl(self,ytid):
        return ytid.replace("/", "_")
    
    def getseries(self, SeriesID):
        _API_SHOW_URL = "https://apiv2.sonyliv.com/AGL/2.6/SR/ENG/WEB/IN/MH/DETAIL-V2/{}?kids_safe=false&from=0&to=49"
        response = self.session.get(_API_SHOW_URL.format(SeriesID),headers=self.Getheaders).json()
        resp = response['resultObj']['containers'][0]['containers']
        season_id = None
        try:
            for season in resp:
                if self.SEASON ==  season['metadata']['season']:
                    season_id = season['id']
                    break
        except Exception as e:
            self.logger.info(e)
            self.logger.info("\nError fetching Season Data!!!")
            raise Exception("Failed to fetch series data")
        if season_id is None:
            raise Exception(f"Season {self.SEASON} not found")
        response = requests.get(f"https://apiv2.sonyliv.com/AGL/2.6/SR/ENG/WEB/IN/MH/CONTENT/DETAIL/BUNDLE/{season_id}?from=0&to=999999&orderBy=episodeNumber&sortOrder=asc&kids_safe=false", headers=self.Getheaders)
        #open("sl.json","w").write(response.text)
        playlist = []
        try:
            response_js = response.json()
            resp = response_js['resultObj']['containers'][0]['containers']
            for episode in resp:
                episode = episode.get('metadata')
                if episode.get('episodeNumber', 0) < self.from_ep:
                    continue
                if self.name == "":
                    self.name = episode['title']
                #ename = episode['episodeTitle']
                edict = {
                    'sno':episode['season'],
                    'number': episode['episodeNumber'],
                    'contentId': episode['contentId'],
                    'name': f'{episode["title"]} S{str(episode["season"]).zfill(2)}E{str(episode["episodeNumber"]).zfill(2)}'
                }
                playlist.append(edict)
                #dont save more than required
                if self.multi_episode:
                    if episode['episodeNumber'] > self.to_ep:
                        break
                else:
                    break
        except:
            self.logger.info(f"{response.text}")
            self.logger.info(f"\nError fetching Episode Data for Season: {season}!!!")
            raise (f"\nError fetching Episode Data for Season: {season}!!!")
        return self.name, playlist
    
    def single(self, FindID):
        if not self.SEASON:
            self.getMovieData(FindID)
            #update ContentID
            FindID = self.mainUrl
        DR = '"UNKNOWN"'
        AUD = '"STEREO"'
        RES = '"848"'
        if self.xcodec == "dolby":
            DR = '"DOLBY_VISION,"'
            AUD = '"DOLBY_ATMOS,"'
            RES = '"2352"'
        if self.xcodec == "h265":   
            AUD = '"DOLBY_5.1,"'
            DR = '"HEVC,"'
            RES = '"2352"'
        if self.xcodec == "h264":  
            RES = '"2352"'
            AUD = '"AAC,"'
            DR = '"HDR10,HLG,HDR10_PLUS,"'
        headers = {
            'authorization': self.TOKEN,
            'user-agent': 'okhttp/4.9.1',
            'content-type': 'application/json',
            'device_id': self.DEVICE_ID,
          #  "App_version": "6.15.60",
            'security_token': self.SecurityToken,
            'td_client_hints': '{"os_name":"Android","os_version":"14","ram":8,"device_type":"phone","device_make":"REDMI","device_model":"REDMI NOTE 12","auto_retry":false,"client_throughput":77,"td_user_useragent":"Dalvik\/2.1.0","display_res":'+RES+',"viewport_res":'+RES+',"supp_codec":"AAC,H264,HEVC,AV1,EAC3,VP9,DOLBY_VISION,DOLBY_ATMOS,","hdr_decoder":'+DR+',"audio_decoder":'+AUD+'}',
        }
        response = self.session.post(
                f'https://apiv2.sonyliv.com/AGL/3.0/SR/ENG/ANDROID_PHONE/IN/KL/CONTENT/VIDEOURL/VOD/{FindID}',
                headers=headers,
            )
        try:
            resp = response.json()['resultObj']
            if 'videoURL' not in resp:
                self.logger.error(resp)
                raise Exception("Failed to get mpd")
            mpd = resp['videoURL']
            KID = None
            lurl = None
            S = resp['subtitle']
            self.sy_subs = []  # Initialize the list
            for x in S:
               self.sy_subs.append({"url": x.get('subtitleUrl'), "lang": x.get('subtitleLanguageName').lower()})
          #  print(self.sy_subs)
            if "drm_video_kid" in resp:
                KID = resp['drm_video_kid']
                if len(KID) < 32:
                    KID = KID + "0" * (32 - len(KID))
            if "LA_Details" in resp:
                if "laURL" in resp["LA_Details"]:
                    lurl = resp["LA_Details"]["laURL"]
        except Exception as e:
            print(e)
            print(response.json())
        if KID and not lurl:
            json_data = {
                'platform': 'web',
                'deviceId': self.DEVICE_ID,
                'actionType': 'play',
                'browser': 'chrome',
                'assetId': int(FindID),
                'os': 'chrome',
            }
            response = self.session.post('https://apiv2.sonyliv.com/AGL/1.4/A/ENG/ANDROID_PHONE/IN/CONTENT/GETLAURL', headers=headers, json=json_data)
            try:
                lurl = response.json()['resultObj']['laURL']
            except Exception as e:
                print(e)
        return mpd, lurl, KID

    async def get_input_data(self):
        """Return:
           title: str
           success: True or False
        """
        if self.SEASON:
            _, self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[0].get('contentId'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)
        if isinstance(tempData, str):
            return tempData, False
        mpdUrl, _, __ = tempData
 #       print(mpdUrl)
        self.MpdDATA = self.parsempd(mpdUrl)
        #logging.info(self.MpdDATA)
        #self.audios = await self.get_audios_ids()
        #self.videos = await self.get_videos_ids()
        return self.name, True

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos
    
    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            episodes = []
            for eps in self.SEASON_IDS:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            only_series_name = self.name + (f" ({self.year})" if self.year!="" else "")
            OUTPUT = os.path.join(self.filedir, only_series_name)
            OUTPUT = OUTPUT.replace(" ", ".")
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                    url, lisence_url, kid_ = self.single(str(x['id']))
                    series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                    spisode_number = series_name.rsplit(" ",1)[1]
                    MpdDATA = self.parsempd(url)
                    if kid_:
                        keys = []
                        pssh = self.GetPssh(kid_)
                        if pssh != "":
                            keys = self.GetKeys(pssh, lisence_url)
                            if not keys:
                                raise Exception('Failed getting keys..!')
                    downloader: Downloader = Downloader(url, OUTPUT, "KAIOS")
                    await downloader.set_data(MpdDATA)
                    await self.edit(f"`[+]` **Downloading Episode:** `{spisode_number}-{self.name}`")
                    await downloader.download(video, audios, custom_header=["x-playback-session-id:81b70ff3-c98c-400a-ac6e-83f0c2ce56c8"])
                    await self.edit(f"`[+]` **Decrypting Episode:** `{spisode_number}-{self.name}`")
                    if kid_:
                        await downloader.set_key(keys)
                        await downloader.decrypt()
                    else:
                        await downloader.no_decrypt()
                    await self.edit(f"`[+]` **Muxing Episode:** `{self.name}.{spisode_number}`")
                    await downloader.merge(series_name + (f" ({self.year})" if self.year!="" else ""), self.id, type_="SonyLiv")
                except Exception as e:
                    await msg.edit(text=e)
                    continue
            
        else:
            try:
                self.COUNT_VIDEOS = 1
                keys = []
                url, lisence_url, kid_ = self.SINGLE
                if kid_:
                    pssh = self.GetPssh(kid_)
                    if pssh != "":
                        keys = self.GetKeys(pssh, lisence_url)
                        if not keys:
                            raise Exception('Failed getting keys..!')
                OUTPUT = os.path.join(self.filedir, self.name)
                OUTPUT = OUTPUT.replace(" ", ".")
                downloader = Downloader(url, OUTPUT, "KAIOS")
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{self.name}`")
                await downloader.download(video, audios, custom_header=["x-playback-session-id:81b70ff3-c98c-400a-ac6e-83f0c2ce56c8"])
                await self.edit(f"`[+]` **Decrypting:** `{self.name}`")
                if kid_:
                    await downloader.set_key(keys)
                    await downloader.decrypt()
                else:
                    await downloader.no_decrypt()
                await self.edit(f"`[+]` **Muxing:** `{self.name}`")
                await downloader.merge(self.name + (f" ({self.year})" if self.year!="" else ""), self.id, type_="SonyLiv")
            except Exception as e:
                await msg.edit(text=e)
                
    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            pass
        
class HotStar:    
    def __init__(self, mainUrl, filedir, mess, token, xcodec="", method=""):
        self.mainUrl = mainUrl.replace("tv", "shows")
        self.raw = ""
        self.token = token
        self.id = mess
        self.url = mainUrl
        self.session = requests.Session()
        self.proxy = {
            'https': HS_PROXY
        }
        self.session.proxies.update(self.proxy)
        self.xcodec = xcodec
        self.method = method
      #  self.refreshUserToken()
        self.logger = logging.getLogger(__name__)
        if "https://" in mainUrl or "http://" in mainUrl:
            mainUrl = mainUrl.split(':', 1)
            self.raw = mainUrl[1].split(':', 1)
            if len(self.raw) == 2:
                mainUrl = self.raw[0]
                self.raw = self.raw[1]
            else:
                mainUrl = self.raw[0]
                self.raw = ""
            try:
                self.mainUrl = mainUrl.split('/')[-1].split("?",1)[-1]
            except Exception as e:
                self.logger.info(mainUrl)
                self.logger.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl
        self.SEASON = None
        self.COUNT_VIDEOS = 0
        self.SINGLE = None
        self.ExtractUrl() # Extracts the session and episode number from the url
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
        self.data = {}
        self.proxies = {}
        self.year = ""
        self.UpdateUserData()
        self.license_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.hotstar.com/',
                'Origin': 'https://www.hotstar.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'TE': 'Trailers',
                }
        self.hotstarPlaybackURL="https://api.hotstar.com/play/v2/playback/content/{contentID}?device-id={userDeviceID}&desired-config=audio_channel:dolby51|encryption:widevine|ladder:tv|package:dash|resolution:4k|subs-tag:HotstarPremium|video_codec:vp9&os-name=Android&os-version=8"
        self.hotstarMovieInfoURL="https://api.hotstar.com/o/v1/movie/detail?tao=0&tas=20&contentId={contentID}"
        self.hotstarShowInfoURL="https://api.hotstar.com/o/v1/show/detail?tao=0&tas=20&contentId={contentID}"
        self.hotstarSeasonInfoURL="https://api.hotstar.com/o/v1/season/detail?tao=0&tas=20&size=5000&id={seasonID}"
        self.url = mainUrl
       # self.TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IiIsImF1ZCI6InVtX2FjY2VzcyIsImV4cCI6MTcwNTM3MDMxNSwiaWF0IjoxNzA1MjgzOTE1LCJpc3MiOiJUUyIsImp0aSI6ImNhMjNiNDBjZDM0YTRiNDViZDU0YzJjNDAyYjlmNTNlIiwic3ViIjoie1wiaElkXCI6XCI1MmVkMzI2ZGNlYmE0YjNkOTI3NWE1NzUwYjcxNGFhNVwiLFwicElkXCI6XCJmYWRjODEyMTI1OWE0Y2JhOTI0MWYxNmM4YmI3OTRmMVwiLFwibmFtZVwiOlwiU3RhcmtcIixcInBob25lXCI6XCI3Mzk2NjM4NTI4XCIsXCJpcFwiOlwiNDMuMjQxLjEyMS4yMFwiLFwiY291bnRyeUNvZGVcIjpcImluXCIsXCJjdXN0b21lclR5cGVcIjpcIm51XCIsXCJ0eXBlXCI6XCJwaG9uZVwiLFwiaXNFbWFpbFZlcmlmaWVkXCI6ZmFsc2UsXCJpc1Bob25lVmVyaWZpZWRcIjp0cnVlLFwiZGV2aWNlSWRcIjpcIjdmMWYwNTMyLTFlYWEtNDM1OC05MjkxLTNlOTg5NWJlZTVmNFwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7XCJIb3RzdGFyUHJlbWl1bVNtcFwiOntcInN0YXR1c1wiOlwiU1wiLFwiZXhwaXJ5XCI6XCIyMDI0LTAyLTE1VDAxOjU3OjQ0LjAwMFpcIixcInNob3dBZHNcIjpcIjBcIixcImNudFwiOlwiMVwifX19LFwiZW50XCI6XCJDZ3NTQ1FnS09BUkFBVkR3RUFyTkFRb0ZDZ01LQVFVU3d3RVNCMkZ1WkhKdmFXUVNBMmx2Y3hJRGQyVmlFZ2xoYm1SeWIybGtkSFlTQm1acGNtVjBkaElIWVhCd2JHVjBkaElFYlhkbFloSUhkR2w2Wlc1MGRoSUZkMlZpYjNNU0JtcHBiM04wWWhJRWNtOXJkUklIYW1sdkxXeDVaaElLWTJoeWIyMWxZMkZ6ZEJJRWRIWnZjeElFY0dOMGRoSURhbWx2R2dKelpCb0NhR1FhQTJab1pCb0NOR3NpQldoa2NqRXdJZ3RrYjJ4aWVYWnBjMmx2YmlJRGMyUnlLZ1p6ZEdWeVpXOHFDR1J2YkdKNU5TNHhLZ3BrYjJ4aWVVRjBiVzl6V0FFS0lnb2FDZzRTQlRVMU9ETTJFZ1UyTkRBME9Rb0lJZ1ptYVhKbGRIWVNCRGhrV0FFSzRBRUtCUW9EQ2dFQUV0WUJFZ2RoYm1SeWIybGtFZ05wYjNNU0EzZGxZaElKWVc1a2NtOXBaSFIyRWdabWFYSmxkSFlTQjJGd2NHeGxkSFlTQkcxM1pXSVNCM1JwZW1WdWRIWVNCWGRsWW05ekVnWnFhVzl6ZEdJU0JISnZhM1VTQjJwcGJ5MXNlV1lTQ21Ob2NtOXRaV05oYzNRU0JIUjJiM01TQkhCamRIWVNBMnBwYnhJRWVHSnZlQklMY0d4aGVYTjBZWFJwYjI0YUFuTmtHZ0pvWkJvRFptaGtHZ0kwYXlJRmFHUnlNVEFpQzJSdmJHSjVkbWx6YVc5dUlnTnpaSElxQm5OMFpYSmxieW9JWkc5c1luazFMakVxQ21SdmJHSjVRWFJ0YjNOWUFSSmNFTURUNzlQYU1ScEtDaHRJYjNSemRHRnlVSEpsYldsMWJTNUpUaTVOYjI1MGFDNHlPVGtTRVVodmRITjBZWEpRY21WdGFYVnRVMjF3R2dSVFpXeG1JTWk0MmRiUU1TakEwKy9UMmpFd0JqZ0JRQU5DQnlpQWpPS3l5ekU9XCIsXCJpc3N1ZWRBdFwiOjE3MDUyODM5MTU3NzcsXCJpbWdcIjpcIjVcIixcImRwaWRcIjpcImZhZGM4MTIxMjU5YTRjYmE5MjQxZjE2YzhiYjc5NGYxXCIsXCJzdFwiOjEsXCJkYXRhXCI6XCJDZ1FJQUJJQUNoSUlBQ0lPZ0FFU2lBRUJrQUg2eGZLODRqQUtCQWdBTWdBS0JBZ0FPZ0FLQkFnQVFnQUtuQUlJQUNxWEFncHdDZ0FTVWdvRGRHVnNHZzBTQlRFME56RTBHUENJLzZrR0doSVNDakV5TmpBd01EVXhNVE1Zd2VXcXBBWWFFaElLTVRJMk1ERTBNRFl4TkJpYitwK2tCaG9VQ0FJU0NtUnBjMjVsZVhCc2RYTVkxcmZpcGdZU0dBb0RaVzVuR2hFSUFSSUhZM0pwWTJ0bGRCaUovb0txQmdvWUNnSUlBaElGQ2dObGJtY1NCUW9EZEdWc0dKR0M5NndHQ21NS0J3Z0JGUUFBQUVBU0Nnb0RkR1ZzSllpY2ZUOFNDZ29EWW1WdUpSaXJpemNTQ2dvRGFHbHVKYlIrc0RvU0Nnb0RiV0ZzSlMxK0p6b1NDZ29EZEdGdEpYamFtVGtTQ2dvRFpXNW5KUlpQNWpzU0Nnb0RhMkZ1SmFPQTBUWVlrWUwzckFZS0VRb0NDQU1TQlFvRGRHVnNHSkdDOTZ3R0NoRUtBZ2dFRWdVS0EyVnVaeGlKL29LcUJnPT1cIn0iLCJ2ZXJzaW9uIjoiMV8wIn0.-4E_l4Kz8Z4cD3IpOwVuOe4nowf96vwcX7bLFQqb2pE"
        self.HEADERS1 = {
            'authority': 'www.hotstar.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'eng',
            'baggage': 'sentry-environment=prod,sentry-release=23.10.16.3-2023-10-19T05%3A14%3A54,sentry-transaction=%2F%5B%5B...slug%5D%5D,sentry-public_key=d32fd9e4889d4669b234f07d232a697f,sentry-trace_id=3afef9264f9f40fbbd320943c65ffe9e,sentry-sample_rate=0',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.hotstar.com',
            'pragma': 'no-cache',
            'referer': 'https://www.hotstar.com/in/shows/loki/1260063451?filters=content_type%3Dshow_clips',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '3afef9264f9f40fbbd320943c65ffe9e-8d52b52b05b5b7a6-0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-country-code': 'in',
            'x-hs-accept-language': 'eng',
            'x-hs-client': 'platform:firetv;app_version:7.41.0;browser:Chrome;schema_version:0.0.911',
            'x-hs-client-targeting': 'ad_id:cb78c6c0-9234-4a1b-a18f-f685afc1705e;user_lat:false',
            'x-hs-device-id': '669da3-311f4f-33070f-841288',
            'x-hs-platform': 'web',
            'x-hs-request-id': '6360c4-7d739e-3a2d6d-223624',
            'x-hs-usertoken': self.get_token(),
            'x-request-id': '6360c4-7d739e-3a2d6d-223624',
        }
        
        self.COOKIES = {
            'device_id': '7f1f0532-1eaa-4358-9291-3e9895bee5f4',
            'hs_uid': 'cb78c6c0-9234-4a1b-a18f-f685afc1705e',
            'userLocale': 'eng',
            'ajs_group_id': 'null',
            'ajs_user_id': '%22cb45c780d2884147a39f6140b3a22b49%22',
            'ajs_anonymous_id': '%2205ceb57a-62ea-469d-91f7-9b2105771713%22',
            'x_migration_exp': 'true',
            'SELECTED__LANGUAGE': 'eng',
            'deviceId': '7f1f0532-1eaa-4358-9291-3e9895bee5f4',
            'userCountryCode': 'in',
            '_gcl_au': '1.1.1337394325.1694078636',
            '_fbp': 'fb.1.1696356044525.311534359',
            '_ga_VJTFGHZ5NH': 'GS1.2.1696354438.31.1.1696356892.56.0.0',
            'userHID': '52ed326dceba4b3d9275a5750b714aa5',
            'userPID': 'fadc8121259a4cba9241f16c8bb794f1',
            '_ga': 'GA1.1.1730233636.1678019100',
            '_uetsid': 'fbb3e910f6e411eea93d5dc9deb0fb8a',
            '_uetvid': 'c04e7620763c11ee971a871c28e137da',
            'userUP': self.get_token(),
            '_ga_QV5FD29XJC': 'GS1.1.1698051247.94.1.1698052065.60.0.0',
            '_ga_EPJ8DYH89Z': 'GS1.1.1698051247.54.1.1698052065.60.0.0',
            '_ga_2PV8LWETCX': 'GS1.1.1698051247.54.1.1698052065.60.0.0',
            'AK_SERVER_TIME': f'{int(time.time())}',
            'appLaunchCounter': '2',
        }
        self.headers={
            'User-Agent': 'Hotstar;in.startv.hotstar/3.3.0 (Android/8.1.0)',
            'hotstarauth': self.get_akamai()[0],
            'X-Country-Code': 'in',
            'X-HS-AppVersion': '3.3.0',
            'X-HS-Platform': 'firetv',
            'X-HS-UserToken': self.get_token(),
            'Cookie': self.get_akamai()[1]
        }

        self.infoHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': '*/*',
            'Accept-Language': 'eng',
            'Referer': 'https://www.hotstar.com/',
            'x-country-code': 'IN',
            'x-platform-code': 'PCTV',
            'x-client-code': 'LR',
            'hotstarauth': self.get_akamai()[0],
            'x-region-code': 'DL',
            'x-hs-usertoken': self.get_token(),
            'Origin': 'https://www.hotstar.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
    
    @staticmethod
    def get_akamai():
        enc_key = b"\x05\xfc\x1a\x01\xca\xc9\x4b\xc4\x12\xfc\x53\x12\x07\x75\xf9\xee"
        st = int(time.time())
        exp = st + 6000
        res = f"st={st}~exp={exp}~acl=/*"
        res += "~hmac=" + hmac.new(enc_key, res.encode(), hashlib.sha256).hexdigest()
        res2 = f"exp={exp}~acl=/*"
        res2 += "~data=hdntl~hmac=" + hmac.new(enc_key, res.encode(), hashlib.sha256).hexdigest()
        return res, res2

    def generateDeviceID(self):
        user_token_json = json.loads(base64.b64decode(self.token.split(".")[1] + "========").decode('utf-8'))
        user_token_json = user_token_json['sub']
        start_index = user_token_json.find('deviceId') + 11
        end_index = user_token_json.find('",', start_index)
        userDeviceID = user_token_json[start_index:end_index]
        HOTSTAR_DEVICE_ID = userDeviceID
        return HOTSTAR_DEVICE_ID

    def get_token(self):
        url = "https://www.hotstar.com/api/internal/bff/p13n/v1/users/watchlist"
        headers = {
               "Accept": "application/json, text/plain, */*",
               "Accept-Encoding": "gzip, deflate, br, zstd",
               "Accept-Language": "eng",
               "Content-Length": "123",
               "Content-Type": "application/json",
               "Cookie": "",
               "Origin": "https://www.hotstar.com",
               "Priority": "u=1, i",
               "Referer": "https://www.hotstar.com/in/mypage",
               "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
               "Sec-Ch-Ua-Mobile": "?0",
               "Sec-Ch-Ua-Platform": "\"Windows\"",
               "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Site": "same-origin",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
               "X-Country-Code": "in",
               "X-Hs-Accept-Language": "eng",                "X-Hs-Client": "platform:web;app_version:24.05.17.1;browser:Chrome;schema_version:0.0.1226;network_data:4g",
               "X-Hs-Client-Targeting": "ad_id:669da3-311f4f-33070f-841288;user_lat:false;",
               "X-Hs-Device-Id": "669da3-311f4f-33070f-841288",
               "X-Hs-Platform": "web",
               "X-Hs-Request-Id": "41ddf1-42bb10-caa30-74ea02",
                "X-Hs-Usertoken": self.token}
        response = self.session.post(url, headers=headers)
        response.raise_for_status()
        try:
          updated_token = response.headers["sessionUserUP"]
       #   print(updated_token)
        except:
          updated_token = self.token
          print ( "token not expired")
         
        return updated_token
     
    def UpdateUserData(self):
        if int(time.time() - Config.HOTSTAR_REFRESH) > 86400 or Config.HOTSTAR_REFRESH == 0.0:
            self.get_token()

    def getResponseData(self, url, headers=None):
        try:
            response=self.session.get(url=url, headers=self.infoHeaders if headers==None else headers, proxies=self.proxies)
            jsonData=json.loads(response.content)
            # self.logger.info(jsonData)
            return jsonData
        except:
            self.logger.info(f"error getting data for url: {self.url}")
            
    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])
      
    def getseries(self, contentID):
        showInfoURL = self.hotstarShowInfoURL.format(contentID=contentID)
        showDataJson = self.getResponseData(showInfoURL, self.infoHeaders)
        seasonData = {}
        season_id = None
        try:
            self.title = showDataJson['body']['results']['item']['title']
            for sData in showDataJson['body']['results']['trays']['items']:
                if(sData['title']=='Seasons'):
                    for season in sData['assets']['items']:
                        if self.SEASON == season['seasonNo']:
                            season_id = season['id']
                            break
            self.logger.info("\nSeason data fetched successfully!!!")
        except Exception as e:
            self.logger.info(e)
            self.logger.info("\nError fetching Season Data!!!")
            return
        if season_id is None:
            raise Exception("Season not found")
        seasonInfoURL=self.hotstarSeasonInfoURL.format(seasonID=season_id)
        episodeDataJson=self.getResponseData(seasonInfoURL)
   
        playlist = []
        try:
            for episode in episodeDataJson['body']['results']['assets']['items']:
                playlist.append({
                        'id': episode['id'],
                        'number': episode['episodeNo'],
                        'name': self.title +  ' ' + 'S{}E{}'.format(self.FixSeq(season['seasonNo']), self.FixSeq(episode['episodeNo'])),
                        'contentId': episode['contentId']
                    })
            self.logger.info(f"\nSeason: {season} episode data fetched successfully!!!")
        except:
            self.logger.info(f"{episodeDataJson}")
            self.logger.info(f"\nError fetching Episode Data for Season: {season}!!!")
            return
        #open("pl.json","w").write(json.dumps(playlist))
        return self.title, playlist  

    def FixSeq(self, seq):
        if int(len(str(seq))) == 1:
            return f'0{str(seq)}'

        return str(seq)
        
    def extract_slug(self, url):
        pattern = r"/in/([^/]+/[^/]+)/(\d+)"
        match = re.search(pattern, url)
        if match:
            found_string = "/in/" + match.group(1) + "/" + match.group(2)
            return found_string  # Output: /in/shows/good-luck-charlie/1260035526
        else:
            print("Match Not Found")
            return

    def get_serie_id(self, url):
        pattern = r"/in/([^/]+/[^/]+)/(\d+)"
        match = re.search(pattern, url)
        
        return match.group(2) if match else None
        
    def single(self, contentID=None, hevc=False):
        if self.xcodec == "4k":
             params = {
                'filters': 'content_type=episode',
                'client_capabilities': '{"ads":["non_ssai"],"audio_channel":["dolbyatmos","dolby51","dolby","stereo"],"container":["fmp4","fmp4br","ts"],"dvr":["short"],"dynamic_range":["sdr"],"encryption":["widevine","plain"],"ladder":["tv"],"package":["dash","hls"],"resolution":["4k","fhd","hd","sd"],"video_codec":["h265"],"audio_codec":["ac4","ec3","aac"],"true_resolution":["4k","sd","hd","fhd"]}',
                'drm_parameters': '{"hdcp_version":["HDCP_V2_2"],"widevine_security_level":["SW_SECURE_DECODE"],"playready_security_level":[]}',
             }
        else:
            params = {
                'filters': 'content_type=episode',
                'client_capabilities': '{"ads":["non_ssai"],"audio_channel":["dolbyatmos","dolby51","dolby","stereo"],"container":["fmp4","fmp4br","ts"],"dvr":["short"],"dynamic_range":["sdr"],"encryption":["widevine","plain"],"ladder":["tv"],"package":["dash","hls"],"resolution":["4k","fhd","hd","sd"],"video_codec":["h264"],"audio_codec":["ac4","ec3","aac"],"true_resolution":["4k","sd","hd","fhd"]}',
                'drm_parameters': '{"hdcp_version":["HDCP_V2_2"],"widevine_security_level":["SW_SECURE_DECODE"],"playready_security_level":[]}',
            }
            
        slug = self.extract_slug(self.url)
        try: 
           api_url = f"https://www.hotstar.com/api/internal/bff/v2/slugs{slug}/a/{contentID}/watch"
           response = self.session.get(
                api_url,
                params=params,
                cookies=self.COOKIES,
                headers=self.HEADERS1,         
                ).json()
         #  print(response)
           mpd = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary']['content_url']
           try:
              license = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary']['license_url']
           except:
                license = ""
        except:
              api_url = f"https://www.hotstar.com/api/internal/bff/v2/slugs/in/movies/a/{contentID}/watch"
              response = self.session.get(
                api_url,
                params=params,
                cookies=self.COOKIES,
                headers=self.HEADERS1,         
                ).json()
            #  print(response)
              mpd = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary']['content_url']
              try:
                 license = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary']['license_url']
              except:
                 license = ""
        json_ld_data = json.loads(response['success']['page']['spaces']['seo']['widget_wrappers'][0]['widget']['data']['json_ld_data']['schemas'][0])
        showTitle = json_ld_data['name']
        if json_ld_data.get("containsSeason", None) is not None:
            seasonNumber = json_ld_data['containsSeason']['seasonNumber']
            episodeNumber = json_ld_data['containsSeason']['episode']['episodeNumber']
            episodeTitle = json_ld_data['containsSeason']['episode']['name']
            name = f"{showTitle} S{int(seasonNumber):02d}E{int(episodeNumber):02d} {episodeTitle}"
        else:
            json_ld_data = json.loads(response['success']['page']['spaces']['seo']['widget_wrappers'][0]['widget']['data']['json_ld_data']['schemas'][1])
            releaseYear = json_ld_data.get('releaseYear', 0)
            name = f"{showTitle} {releaseYear}"
        name = name.replace("(", " ").replace(")", " ")
        return mpd, license, name            
            
    def fix_id_ytdl(self,ytid):
        return ytid.replace("/", "_")

    async def parse_m3u8(self, m3u8):
        """It will extract all the data from link"""
        try:
            yt_data = ytdl.YoutubeDL(
                                     {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True, 'proxy' : proxy}).extract_info(
                                     m3u8,
                                     download=False)
            formats = yt_data.get('formats', None)
            data = {}
            data["videos"] = []
            data["audios"] = []
            data["pssh"] = ''
            data["subtitles"] = []
            if formats:
                for i in formats:
                    format_id = i.get('format_id', '')
                    is_video = i.get("video_ext", "none") != "none"
                    is_audio = i.get("audio_ext", "none") != "none"
                    if is_audio:
                        data["audios"].append({"lang": i.get("language", "default") + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
                    if is_video:
                        data["videos"].append({"height": str(i.get("height", "default")) + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
            else:
                raise Exception("Error in getting data")
            return data
        except Exception as e:
            raise Exception(e)
    
    async def parsempd(self, MpdUrl, msg=None):
        if ".mpd" not in MpdUrl or ".m3u8" in MpdUrl:
            return await self.parse_m3u8(MpdUrl)
        audioslist = []
        videoslist = []
        subtitlelist = []
        pssh = ""
     #   print(MpdUrl)
        mpdHeaders= {
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "KAIOS/2.0",
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        mpd = self.session.get(MpdUrl, headers=mpdHeaders, proxies=self.proxies)
        if mpd.status_code != 200:
            mpdPath = f'mpd-{time.time()}.txt'
            m = subprocess.run(["aria2c", MpdUrl, '-o', mpdPath, '-U', 'KAIOS'])
            if os.path.exists(mpdPath):
                with open(mpdPath) as f:
                    mpd = f.read()
                    f.close()
                os.remove(mpdPath)
            else:
                self.logger.error('failed downloading mpd with aria2c too..!')
                raise Exception("")
        else:
            mpd = mpd.text
        if mpd:
            mpd = re.sub(r"<!--  -->","",mpd)
            mpd = re.sub(r"<!-- Created+(..*)","",mpd)		
            mpd = re.sub(r"<!-- Generated+(..*)","",mpd)
        try:
            mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        except:
            if "#EXTM3U" in mpd.upper():
                return await self.parse_m3u8(MpdUrl)
            self.logger.info(str(mpd))
            raise "Failed to parse mpd"
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        baseurl = MpdUrl.rsplit('master')[0]
     #   print(baseurl)
        try:
            for ad in AdaptationSet:
                if ad['@mimeType'] == 'video/mp4' or ad['@mimeType'] == "audio/mp4":
                    if 'ContentProtection' not in ad:
                        continue
                    for protections in ad['ContentProtection']:
                        if protections['@schemeIdUri'] == 'urn:uuid:EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED' or protections['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh=protections['cenc:pssh']
        except Exception as e:
            self.logger.info("Failed to get pssh, probably not encrypted")
            pssh = ""
        for ad in AdaptationSet:
            if ad['@mimeType'] == "audio/mp4":
                try:
                    auddict = {
                    'id': self.fix_id_ytdl(ad['Representation']['@id']),
                    'codec': ad['Representation']['@codecs'],
                    'bandwidth': ad['Representation']['@bandwidth'],
                    'lang': ad.get('@lang',"Default") + " " + f"({fix_codec_name(ad['Representation']['@codecs'])} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                    }
                    audioslist.append(auddict)
                except Exception:
                    for item in ad['Representation']:
                        auddict = {
                        'id': self.fix_id_ytdl(item['@id']),
                        'codec': item['@codecs'],
                        'bandwidth': item['@bandwidth'],
                        'lang': ad.get('@lang',"Default") + " " + f"({fix_codec_name(item['@codecs'])} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        audioslist.append(auddict)

            if ad['@mimeType'] == "video/mp4":
                for item in ad['Representation']:
                    viddict = {
                    'width': item['@width'],
                    'height': item['@height'] + f" - {bandwith_convert(item['@bandwidth'])}",
                    'id': self.fix_id_ytdl(item['@id']),
                    'codec': item['@codecs'],
                    'bandwidth': item['@bandwidth']
                    }
                    videoslist.append(viddict)

            if ad['@mimeType'] == "text/vtt":
                subdict = {
                'id': self.fix_id_ytdl(ad['Representation']['@id']),
                'lang': ad['@lang'],
                'bandwidth': ad['Representation']['@bandwidth'],
                'sub_url' : ad['Representation']['BaseURL'],
                'url': baseurl + ad['Representation']['BaseURL']
                }
                subtitlelist.append(subdict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist, "pssh": pssh}
        return all_data
    
    def Get_PSSH(self, mp4_file):
        WV_SYSTEM_ID = '[ed ef 8b a9 79 d6 4a ce a3 c8 27 dc d5 1d 21 ed]'
        pssh = None
        data = subprocess.check_output(["mp4dump", '--format', 'json', '--verbosity', '1', mp4_file])
        data = json.loads(data)
        for atom in data:
            if atom['name'] == 'moov':
                for child in atom['children']:
                    if child['name'] == 'pssh' and child['system_id'] == WV_SYSTEM_ID:
                        pssh = child['data'][1:-1].replace(' ', '')
                        pssh = binascii.unhexlify(pssh)
                        pssh = pssh[0:]
                        pssh = base64.b64encode(pssh).decode('utf-8')
                        return pssh

    def getWidevineKeys(self, pssh, licurl):
        certData=b'\x08\x04'
        certResponse=self.session.post(url=licurl, data=certData, headers=self.license_headers, proxies=self.proxies)
        certDecoded=certResponse.content
        # self.logger.info(certDecoded)
        certB64=base64.b64encode(certDecoded)
        wvdecrypt=WvDecryptCustom(pssh, certB64, deviceconfig.device_nexus6_lvl1)
        chal=wvdecrypt.get_challenge()
        resp=requests.post(url=licurl, data=chal, headers=self.license_headers, proxies=self.proxies)
        license_decoded=resp.content
        license_b64=base64.b64encode(license_decoded)
        wvdecrypt.update_license(license_b64)
        check_, keys=wvdecrypt.start_process()
        if(check_):
            return keys
        else:
            self.logger.info('Error getting Keys!')
            return []
    
    async def get_input_data(self):
        """Return:
           title: str
           success: True or False
        """
        if self.SEASON:
            _, self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[self.from_ep-1].get('contentId'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)
        if isinstance(tempData, str):
            return tempData, False
        mpdUrl, licenseURL, title = tempData
        self.MpdDATA = await self.parsempd(mpdUrl)
        #self.audios = await self.get_audios_ids()
        #self.videos = await self.get_videos_ids(
        return title, True

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos           

    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            episodes = []
          #  print(episodes)
            seriesname, IDs = self.getseries(self.mainUrl)
            for eps in IDs:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'contentId': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'contentId': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                   url, licenseURL, title= self.single(str(x['contentId']))
                   series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                   spisode_number = series_name.rsplit(" ",1)[1]
                   OUTPUT = os.path.join(self.filedir, seriesname)
                   OUTPUT = OUTPUT.replace(" ", ".")
                   MpdDATA = await self.parsempd(url)
                   keys = []
                   is_drm = False
                   if licenseURL != "":
                      pssh = MpdDATA["pssh"]
                      if pssh != "":
                         for x in range(5):
                             keys = self.getWidevineKeys(pssh, licenseURL)
                             if keys:
                                break
                             await asyncio.sleep(5)
                      is_drm = True
                   downloader = Downloader(url, OUTPUT, "KAIOS", self.xcodec, self.method)
                   await downloader.set_data(MpdDATA)
                   await self.edit(f"`[+]` **Downloading Episode:** `{spisode_number}-{self.title}`")
                   await downloader.download(video, audios)
                   await self.edit(f"`[+]` **Decrypting Episode:** `{spisode_number}-{self.title}`")
                   if is_drm:
                      if keys == []:
                          video_path = os.path.join(os.getcwd(), downloader.TempPath, "jv_drm_video_" + '.mp4')
                          pssh = self.Get_PSSH(video_path)
                          keys = self.getWidevineKeys(pssh, licenseURL)
                      await downloader.set_key(keys)
                      await downloader.decrypt()
                   else:
                       await downloader.no_decrypt()
                   await self.edit(f"`[+]` **Muxing Episode:** `{self.title}.{spisode_number}`")
                   await downloader.merge(series_name, self.id, type_="DSNP")
                except Exception as e:
                    await msg.edit(text=e)
                    continue
        else:
            try:
                self.COUNT_VIDEOS = 1
                url, licenseURL, title = self.SINGLE
                keys = []
                is_drm = False
                if licenseURL != "":
                    pssh = self.MpdDATA["pssh"]
                    if pssh != "":
                        for x in range(5):
                            keys = self.getWidevineKeys(pssh, licenseURL)
                       #     self.log.info(keys)
                            if keys:
                                break
                            await asyncio.sleep(5)
                    is_drm = True 
                OUTPUT = os.path.join(self.filedir, title)
                OUTPUT = OUTPUT.replace(" ", ".")
                downloader = Downloader(url, OUTPUT, "KAIOS", self.xcodec, self.method)
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{title}`")
                await downloader.download(video, audios)
                await self.edit(f"`[+]` **Decrypting:** `{title}`")
                if is_drm:
                    if keys == []:
                        video_path = os.path.join(os.getcwd(), downloader.TempPath, "jv_drm_video_" + '.mp4')
                        pssh = self.MpdDATA["pssh"]
                        keys = self.getWidevineKeys(pssh, licenseURL)
                    await downloader.set_key(keys)
                    await downloader.decrypt()
                else:
                    await downloader.no_decrypt()
                await self.edit(f"`[+]` **Muxing:** `{title}`")
                await downloader.merge(title, self.id, type_="DSNP")
            except Exception as e:
                print(e)
                
    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            pass

class JioCinema:
    def __init__(self, mainUrl, filedir, mess, xcodec=""):
        self.mainUrl = mainUrl
        self.raw = ""
        try:
            temp = xcodec.split("-")
            xcodec = temp[0]
            asset_lang = temp[1]
            print(asset_lang)
        except:
           asset_lang = ""
        self.asset_lang = asset_lang
        self.id = mess
        self.session = requests.Session()
        proxies = {
            'https': proxy
        }
        self.session.proxies.update(proxies)
        self.xcodec = xcodec
        self.logger = logging.getLogger(__name__)
        if "https://" in mainUrl or "http://" in mainUrl:
            mainUrl = mainUrl.split(':', 1)
            self.raw = mainUrl[1].split(':', 1)
            if len(self.raw) == 2:
                mainUrl = self.raw[0]
                self.raw = self.raw[1]
            else:
                mainUrl = self.raw[0]
                self.raw = ""
            try:
                self.mainUrl = mainUrl.rsplit('/', 1)[-1].split("?",1)[0]
            except Exception as e:
                self.logger.info(mainUrl)
                self.logger.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl
        self.SEASON = None
        self.COUNT_VIDEOS = 0
        self.SINGLE = None
        self.ExtractUrl() # Extracts the session and episode number from the url
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
        self.data = {}
        self.proxies = {}
        self.auth_token = Config.JIO_CINEMA_TOKEN
        self.year = ""
        self.title = ""
    
    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])
    
    @property
    def get_headers(self):
        headers = {
            'authority': 'content-jiovoot.voot.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.jiocinema.com',
            'referer': 'https://www.jiocinema.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        return headers

    @property
    def get_token(self):
        headers = {
            'authority': 'auth-jiocinema.voot.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'accesstoken': self.auth_token,
            'content-type': 'application/json',
            'origin': 'https://www.jiocinema.com',
            'referer': 'https://www.jiocinema.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        json_data = {
            'appName': 'RJIL_JioCinema',
            'deviceId': '57650490',
            'refreshToken': '188bbfac-848e-4a6c-99f1-53a14d10877c',
            'appVersion': '5.1.0',
        }

        response = self.session.post('https://auth-jiocinema.voot.com/tokenservice/apis/v4/refreshtoken', headers=headers, json=json_data)
        refresh_token = response.json()['authToken']
        return refresh_token

    def get_title_details(self, title_id):
        response = self.session.get(f'https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/content/query/asset-details?&ids=include:{title_id}&responseType=common&devicePlatformType=desktop',headers=self.get_headers)
        response.raise_for_status()
        json_response = response.json()['result'][0]
        if json_response['mediaType'] == "EPISODE":
           show_name = json_response['showName']
           year = json_response['releaseYear']
           sno = json_response['season'].zfill(2)
           epno = json_response['episode'].zfill(2)
           ep_name = json_response['fullTitle']
           self.title = f"{show_name} {year} S{sno}E{epno} {ep_name}"
        else:
          title = json_response['fullTitle']
          self.year = json_response['releaseYear']
          self.title = f"{title} {self.year}"
        return self.title 
     
    def getseries(self, id_):
        headers = {
            "authority": "content-jiovoot.voot.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "app-version": "5.6.1",
            "origin": "https://www.jiocinema.com",
            "referer": "https://www.jiocinema.com/",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        res = self.session.get(
            f"https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/view/show/{id_}?&responseType=common&features=include:buttonsTray&premiumTrays=false&devicePlatformType=desktop",
            headers=headers
        )       
        episode_list = []
        for tray in res.json()['trays']:
           if tray["title"] == "Episodes" and tray.get('trayTabs', None) is not None:
               sid = tray['trayTabs']
        for a in sid:
            if a["label"] != f"Season {self.SEASON}":
                continue
            for s in range(1, 100):
                params = {
                'sort': 'episode:asc',
                'id': a['id'],
                'responseType': 'common',
                'page': s,
                
                   }

                res = self.session.get(
                'https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/content/generic/series-wise-episode',
                params=params,
                headers=headers,
                )
                result = res.json()["result"]
                if len(result) == 0:
                    break
                for r in result:
                    if self.title == "":
                        self.year = r["releaseYear"] if "releaseYear" in r else ''
                        self.title = r["showName"]
                    if int(r["season"]) != self.SEASON:
                        continue
                    episode_data = {
                            'sno':r['season'],
                            'number': r['episode'],
                            'extid': r["externalId"],
                            'id': r['jioMediaId'], #r['shortTitle'], r["showId"]
                            'name': f'{r["showName"]} S{str(r["season"]).zfill(2)}E{str(r["episode"]).zfill(2)}'
                        }
                    episode_list.append(episode_data)
        return episode_list

    def jc_headers(self):
        if self.xcodec == "dolby":
            headers = {
            'accesstoken': self.get_token,
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-platform': 'androidmobile',
            }
            json_data = {
              "ageGroup": "18+",
              "x-apisignatures": "o668nxgzwff",
              "appVersion": "24.03.300-d53ce23331",
              "bitrateProfile": "xxxhdpi",
              "capability": {
                "drmCapability": {
                  "aesSupport": "none",
                  "fairPlayDrmSupport": "L1",
                  "playreadyDrmSupport": "none",
                  "widevineDRMSupport": "L1"
                },
                "frameRateCapability": [
                ]
              },
              "continueWatchingRequired": False,
              "dolby": True,
              "downloadRequest": False,
              "4k": True,
              "hevc": True,
              "kidsSafe": False,
              "manufacturer": "INFINIX",
              "model": "Infinix",
              "multiAudioRequired": True,
              "osVersion": "13",
              "parentalPinValid": True
              }
        else:
            headers = {
            'accesstoken': self.get_token,
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-platform': 'androidtv',
            'Deviceid': 'b7d39a8f-337e-4d3f-9bc6-41dbbbab8d61'       
            }
            json_data = {
              "ageGroup": "18+",
              "x-apisignatures": "o668nxgzwff",
              "appVersion": "24.03.300-d53ce23331",
              "bitrateProfile": "xhdpi",
              "capability": {
                "drmCapability": {
                  "aesSupport": "yes",
                  "fairPlayDrmSupport": "L1",
                  "playreadyDrmSupport": "none",
                  "widevineDRMSupport": "L1"
                },
                "frameRateCapability": [
                  {
                    "frameRateSupport": "30fps",
                    "videoQuality": "1440p"
                  }
                ]
              },
              "continueWatchingRequired": False,
              "dolby": False,
              "downloadRequest": False,
              "4k": False,
              "hevc": False,
              "kidsSafe": False,
              "manufacturer": "unknown",
              "model": "sdk_google_atv_x86",
              "multiAudioRequired": True,
              "osVersion": "13",
              "parentalPinValid": True
              }
        return headers, json_data

    def single(self, movie_id):
        if not self.SEASON:
            self.get_title_details(movie_id)
        headers, json_data = self.jc_headers()
        manifest_details = None
        m3u8 = ""
        mpd = ""
        lic_url = ""
        response = self.session.post(f'https://apis-jiovoot.voot.com/playbackjv/v5/{movie_id}', headers=headers, json=json_data)
      #  print(response.json())
        if self.asset_lang:
           for id in response.json()['data']['assetsByLanguage']:
               if id['id'] == self.asset_lang:
                  movie_id = id['assetId']
                  print(movie_id)
                  response = self.session.post(f'https://apis-jiovoot.voot.com/playbackjv/v5/{movie_id}', headers=headers, json=json_data)
        if response.json()['code'] == 200:
            for x in response.json()['data']['playbackUrls']:
                if x['streamtype'] == 'hls':
                    m3u8 = x['url']
                elif x['streamtype'] == 'dash':
                    mpd = x['url']
                    lic_url = x['licenseurl']
            if mpd != "":
                m3u8 = ""
            manifest_details = {'mpd': mpd, 'm3u8': m3u8, 'lic_url': lic_url}
        else:
            return 'Some errors occured while parsing manifest..'
        return manifest_details
    
    def decrypt_keys(self, pssh, lic_url):
        headers = {
    
            'accesstoken': self.get_token,
            'content-type': 'application/octet-stream',
            'appname': 'RJIL_JioCinema',
            'deviceid': '57650490',
            'user-agent': 'JioCinema/4.1.3 (Linux;Android 9) 2.18.1',
            'x-platform': 'androidtv',
            'x-feature-code': 'ytvjywxwkn',
            'x-playbackid': '8b99a3a3-10b5-4ca0-9adc-473cbfd5abb8'
            
        }
        wvdecrypt = WvDecrypt(pssh)
        raw_challenge = wvdecrypt.get_challenge()
        widevine_license = self.session.post(
        url=lic_url, headers=headers, data=raw_challenge, timeout=10)
        license_b64 = b64encode(widevine_license.content)
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()
        newkeys = []
        for key in keys:
            if key.type == 'CONTENT':
                newkeys.append('{}:{}'.format(key.kid.hex(), key.key.hex()))
        if newkeys:
            return newkeys 
    
    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        if (len(list_of_audios) == 1 and key) or (len(list_of_audios) == 0 and not key):
            list_of_audios.append("Default")
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos
    
    async def get_input_data(self):
        """Return:
           title: str
           success: True or False
        """
        if self.SEASON:
            self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[self.from_ep-1].get('id'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)
        if isinstance(tempData, str):
            return tempData, False
        if tempData["m3u8"] != "":
            self.MpdDATA = await self.parse_m3u8(tempData["m3u8"])
        elif tempData["mpd"] != "":
            self.MpdDATA = await self.parsempd(tempData["mpd"])
        else:
            return "Error in getting data", False
    #    print(self.MpdDATA)
        #self.audios = await self.get_audios_ids()
        #self.videos = await self.get_videos_ids()
        return self.title + (f" ({self.year})" if self.year != "" else ""), True

    async def parse_m3u8(self, m3u8):
        """It will extract all the data from link"""
        try:
            yt_data = ytdl.YoutubeDL(
                                     {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True, 'proxy' : proxy}).extract_info(
                                     m3u8,
                                     download=False)
            formats = yt_data.get('formats', None)
            data = {}
            data["videos"] = []
            data["audios"] = []
            data["pssh"] = ''
            data["subtitles"] = []
            if formats:
                for i in formats:
                    format_id = i.get('format_id', '')
                    is_video = i.get("video_ext", "none") != "none"
                    is_audio = i.get("audio_ext", "none") != "none"
                    if is_audio:
                        data["audios"].append({"lang": i.get("language", "default") + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
                    if is_video:
                        data["videos"].append({"height": str(i.get("height", "default")) + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
            else:
                raise Exception("Error in getting data")
            return data
        except Exception as e:
          #  print("error")
            raise Exception(e)
          #  print(m3u8)

    async def parsempd(self, MpdUrl):
        self.logger.info(MpdUrl)
        audioslist = []
        videoslist = []
        subtitlelist = []
        pssh = ""
        MpdUrl = MpdUrl.replace("\n" ,"").replace(" ", "").replace("\n\n", "")
        mpd = self.session.get(MpdUrl, headers=self.get_headers).text
        if mpd:
            mpd = re.sub(r"<!--  -->","",mpd)
            mpd = re.sub(r"<!-- Created+(..*)","",mpd)		
            mpd = re.sub(r"<!-- Generated+(..*)","",mpd)
        mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        baseMpd, mpdArgs = MpdUrl.split('?',1)
        baseMpd = baseMpd.rsplit('/',1)[0]
        def get_base(url):
            return baseMpd + "/" + url.split("?",1)[0] + "?" + mpdArgs
        for ad in AdaptationSet:
            if pssh == "" and (('@contentType' in ad and (ad['@contentType'] == "audio" or ad['@contentType'] == "video")) or ('@mimeType' in ad and (ad['@mimeType'] == "audio/mp4" or ad['@mimeType'] == "audio/mp4"))):
                if ad.get('ContentProtection', []) != []:
                    for y in ad.get('ContentProtection'):
                        if str(y.get('@schemeIdUri')).lower() == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh = y.get('cenc:pssh')
                if isinstance(ad['Representation'], list):
                    for item in ad['Representation']:
                        if item.get('ContentProtection', None) is None:
                            continue
                        for y in item.get('ContentProtection', []):
                            if y == None:
                                continue
                            if str(y.get('@schemeIdUri')).lower() == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                                pssh = y.get('cenc:pssh')
            if ('@mimeType' in ad and ad['@mimeType'] == "audio/mp4") or ('@contentType' in ad and (ad['@contentType'] == "audio")):
                try:
                    auddict = {
                    'id': ad['@id'],
                    'codec': ad['@codecs'],
                    'bandwidth': ad['@bandwidth'],
                    'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['@codecs'])} - {bandwith_convert(['@bandwidth'])})"
                    }
                    if "BaseURL" in ad:
                       auddict["url"] = get_base(ad["BaseURL"])
                    audioslist.append(auddict)
                except Exception:
                    if isinstance(ad['Representation'], dict):
                        codec_ = ad['Representation']['@codecs'] if '@codecs' in ad['Representation'] else ad['@codecs']
                        try:
                            lang_ = ad['Representation']['@lang'] if '@lang' in ad['Representation'] else ad['@lang']
                        except:
                            lang_ = "Default"
                        auddict = {
                        'id': ad['Representation']['@id'],
                        'codec': codec_,
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'lang': lang_ + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        if "BaseURL" in ad['Representation']:
                            auddict["url"] = get_base(ad['Representation']["BaseURL"])
                        audioslist.append(auddict)
                    if not isinstance(ad['Representation'], list):
                        continue
                    for item in ad['Representation']:
                        codec_ = ad['@codecs'] if '@codecs' in ad else item['@codecs']
                        try:
                            lang_ = ad['Representation']['@lang'] if '@lang' in ad['Representation'] else ad['@lang']
                        except:
                            lang_ = "Default"
                        auddict = {
                        'id': item['@id'],
                        'codec': codec_,
                        'bandwidth': item.get('@bandwidth', ad.get('@bandwidth', "unknown")),
                        'lang': lang_ + " " + f"({fix_codec_name(codec_)} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        if "BaseURL" in item:
                            auddict["url"] = get_base(item["BaseURL"])
                        audioslist.append(auddict)

            if ('@mimeType' in ad and ad['@mimeType'] == "video/mp4") or ('@contentType' in ad and ad['@contentType'] == "video"):
                for item in ad['Representation']:
                    viddict = {
                    'width': item.get('@width', ad.get('@width', "unknown")),
                    'height': item.get('@height', ad.get('@height', "unknown")) + f" - {bandwith_convert(item['@bandwidth'])}",
                    'id': item['@id'],
                    'codec': item.get('@codecs'),
                    'bandwidth': item['@bandwidth']
                    }
                    if "BaseURL" in item:
                        viddict["url"] = get_base(item["BaseURL"])
                    videoslist.append(viddict)

            if ('@mimeType' in ad and ad['@mimeType'] == "text/vtt") or ('@contentType' in ad and ad['@contentType'] == "text"):
                try:
                    subdict = {
                        'id': ad['@id'] + " " + f"({bandwith_convert(ad['@bandwidth'])})",
                        'lang': ad['@lang'],
                        'bandwidth': ad['@bandwidth'],
                        'url': get_base(ad['BaseURL'])
                        }
                    subtitlelist.append(subdict)
                except Exception:
                    try:
                        subdict = {
                        'id': ad['Representation']['@id'],
                        'bandwidth': ad['Representation']['@bandwidth'],
                        'url': get_base(ad['Representation']['BaseURL']),
                        'lang': ad['@lang'] + " " + f"({bandwith_convert(ad['Representation']['@bandwidth'])})"
                        }
                        subtitlelist.append(subdict)
                    except:
                        if not isinstance(ad['Representation'], list):
                            continue
                        for item in ad['Representation']:
                            subdict = {
                            'id': item['@id'],
                            'bandwidth': item['@bandwidth'],
                            'url': get_base(item['BaseURL']),
                            'lang': ad['@lang'] + " " + f"({bandwith_convert(item['@bandwidth'])})"
                            }
                            subtitlelist.append(subdict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist, "pssh": pssh}
        return all_data
    
    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        custom_header = ["Referer:https://www.jiocinema.com/", "Origin:https://www.jiocinema.com", "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"]
        if self.SEASON:
            episodes = []
            for eps in self.SEASON_IDS:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                   mpddata = self.single(str(x['id']))
                   series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                   spisode_number = series_name.rsplit(" ",1)[1]
                   OUTPUT = os.path.join(self.filedir, self.title)
                   OUTPUT = OUTPUT.replace(" ", ".")
                   licenseURL = mpddata["lic_url"]
                   if mpddata["m3u8"] != "":
                      url = mpddata["m3u8"]
                      MpdDATA = await self.parse_m3u8(mpddata["m3u8"])
                   else:
                      url = mpddata["mpd"]
                      MpdDATA = await self.parsempd(mpddata["mpd"])
                   keys = []
                   is_drm = False
                   if licenseURL != "":
                       pssh = MpdDATA["pssh"]
                       if pssh != "":
                          keys = self.decrypt_keys(pssh, licenseURL)
                       is_drm = True
                   downloader = Downloader(url, OUTPUT, "KAIOS", self.xcodec)
                   await downloader.set_data(MpdDATA)
                   await self.edit(f"`[+]` **Downloading Episode:** `{spisode_number}-{self.title}`")
                   await downloader.download(video, audios)
                   await self.edit(f"`[+]` **Decrypting Episode:** `{spisode_number}-{self.title}`")
                   if is_drm:
                      await downloader.set_key(keys)
                      await downloader.decrypt()
                   else:
                      await downloader.no_decrypt()
                   await self.edit(f"`[+]` **Muxing Episode:** `{self.title}.{spisode_number}`")
                   await downloader.merge(series_name, self.id, type_="Jio")
                except:
                    continue 
        else:
            try:
                self.COUNT_VIDEOS = 1
                licenseURL = self.SINGLE["lic_url"]
                if self.SINGLE["m3u8"] != "":
                    url = self.SINGLE["m3u8"]
                else:
                    url = self.SINGLE["mpd"]
                keys = []
                is_drm = False
                if licenseURL != "":
                    pssh = self.MpdDATA["pssh"]
                    if pssh != "":
                        keys = self.decrypt_keys(pssh, licenseURL)
                        is_drm = True
                OUTPUT = os.path.join(self.filedir, self.title)
                OUTPUT = OUTPUT.replace(" ", ".")
                downloader = Downloader(url, OUTPUT, "KAIOS", self.xcodec)
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{self.title}`")
                await downloader.download(video, audios)
                await self.edit(f"`[+]` **Decrypting:** `{self.title}`")
                if is_drm:
                    await downloader.set_key(keys)
                    await downloader.decrypt()
                else:
                    await downloader.no_decrypt()
                await self.edit(f"`[+]` **Muxing:** `{self.title}`")
                await downloader.merge(self.title + (f" ({self.year})" if self.year!="" else ""), self.id, type_="Jio")
            except Exception as e:
                await msg.edit(text=e)
                
    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            pass


class Zee5:
    def __init__(self, mainUrl, filedir, mess, token, xcode):
        self.xcodec = xcode
        self.token = token
        self.raw = ""
        self.id = mess
        self.session = requests.Session()
        proxies = {
            'https': Z5_PROXY
        }
        self.session.proxies.update(proxies)
        if "https://" in mainUrl or "http://" in mainUrl:
            if ":" in mainUrl:
                mainUrl = mainUrl.split(':', 1)[1]
                if ":" in mainUrl:
                    self.raw = mainUrl.split(':', 1)[1]
                    mainUrl = mainUrl.split(':', 1)[0]
            try:
                self.mainUrl = mainUrl.split('/')[-1]
            except Exception as e:
                logging.info(mainUrl)
                logging.error(e, exc_info=True)
                raise Exception(e)
        else:
            if ":" in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl

        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        self.log = logging.getLogger(__name__)
        self.SEASON = None
        self.proxies = {}
        self.COUNTRY = "IN"
        self.ExtractUrl() # Extracts the session and episode number from the url
        self.tk = self.token
        self.TOKEN = f"bearer {self.token}"
        self.SESSION = self.get_session()
        self.USER_SELECTED_AUDIOS = []
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.COUNT_VIDEOS = 0

    def get_token(self):
        if Config.ZEE5_TOKEN:
            return Config.ZEE5_TOKEN
        else:
            if Config.ZEE5_EMAIL and Config.ZEE5_PASS:
                    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36", 'Content-Type': 'application/json'}
                    data = {"email": Config.ZEE5_EMAIL, "password": Config.ZEE5_PASS,"aid":"91955485578","lotame_cookie_id":"","guest_token":"iuGMwSMz0HdoCQ3jrLP1000000000000","platform":"app","version":"2.51.37"}
                    token = self.session.post('https://whapi.zee5.com/v1/user/loginemail_v2.php', data=json.dumps(data), headers=headers, proxies=self.proxies).json()['access_token']
                    Config.ZEE5_TOKEN = token
                    return token
    
    def get_session(self, series=False):
   #     if not series:
        session_token = requests.get("https://launchapi.zee5.com/launch?ccode=IN&country=IN&translation=en&version=5.0&platform_name=android_app&state=MH", proxies=self.proxies).json()["platform_token"]["token"]
        return session_token
   #     Hacked Token with no expiry
     #   return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTEwLTE1VDA2OjMxOjI2LjE0MVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5NzM1MTQ4Nn0.ITgD4KwHd1mU9g6JDC0LESJpfjJeyD15kGojHLtpkDg"


    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-',1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])

    def do_decrypt(self, pssh, drmdata, nl):
        wvdecrypt = WvDecrypt(pssh)
        chal = wvdecrypt.get_challenge()
        headers = {
                    'origin': 'https://www.zee5.com',
                    'referer': 'https://www.zee5.com/',
                    'customdata': drmdata,
                    'nl': nl,                
                    }
        resp = self.session.post('https://spapi.zee5.com/widevine/getLicense', data=chal, headers=headers, proxies=self.proxies)
        lic = resp.content
        license_b64 = base64.b64encode(lic).decode('utf-8') 
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()
        newkeys = []
        for key in keys:
            if key.type == 'CONTENT':
                newkeys.append('{}:{}'.format(key.kid.hex(), key.key.hex()))
        return newkeys

    def get_headers(self):
        headers = {
            'authority': 'spapi.zee5.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.zee5.com',
            'referer': 'https://www.zee5.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        }
        return headers

    def getPlatformToken(self):
        headers = {
            'user-agent': 'okhttp/4.9.1'
        }
        response = requests.get('https://b2bapi.zee5.com/launch_api/launch_api.php?ccode=IN&lang=en&version=3&country=IN&translation=en&platform_name=androidtv_app', headers=headers)
        if not response.ok:
            print("Get Platform Token Failed: \n", response.text)
         
        platform_token = json.loads(response.content)["platform_token"]["token"]
        return platform_token
  
    def get_title_details(self):
        device_token = self.token
        device_id = "68a30cfb-6fb3-4738-b0f5-c772ec59d450"
        platform_token = self.getPlatformToken()
        json_data = {
            "x-access-token": platform_token,
            "Authorization": f'bearer {device_token}'
        }
        response = self.session.post(f'https://spapi.zee5.com/singlePlayback/getDetails/secure?content_id={self.mainUrl}&device_id={device_id}&check_parental_control=false&country=IN&platform_name=ctv_android', headers=self.get_headers(), json=json_data)
        response.raise_for_status()
        json_response = json.loads(response.content)
        print(json_response)
        return json_response
      
    def getseries(self, seriesID):
        playlist = []
        api = 'https://gwapi.zee5.com/content/tvshow/'
        series_params = {
            'translation': 'en',
            'country': self.COUNTRY
        }
        SeasonNo = self.SEASON
        res = self.session.get(api+seriesID, params=series_params, headers={'x-access-token': self.get_session(True)}, proxies=self.proxies).json()
        seriesname = res.get('title')
        for season in res.get('seasons'):
            if int(SeasonNo) == int(season.get('index')):
                seasonID = season.get('id')
        
        for num in itertools.count(1):
            season_params = {
                'season_id': seasonID,
                'translation': 'en',
                'country': self.COUNTRY,	
                'type': 'episode',
                'on_air': 'true',
                'asset_subtype': 'tvshow',
                'page': num,
                'limit': 25
            }
            res = requests.get(api, params=season_params, headers={'x-access-token': self.get_session(True)}, proxies=self.proxies).json()
            if "error_msg" in res:
                print(res)
                raise Exception(res)
            episodesCount = res.get('total_episodes')
            for item in res.get('episode'):
                episodeNo = item.get('episode_number')
                episodeID = item.get('id')
                seasonNo = season.get('index')
                try:
                    playlist.append({
                        'id': episodeID,
                        'number': episodeNo,
                        'name': seriesname + ' ' + 'S{}E{}'.format(self.FixSeq(seasonNo), self.FixSeq(episodeNo))
                    })
                except Exception:
                    continue

            if not res.get('next_episode_api'):
                break
        
        return seriesname, playlist
    
    def FixSeq(self, seq):
        if int(len(str(seq))) == 1:
            return f'0{str(seq)}'

        return str(seq)
    
    def single(self, id):
        PLAYBACK_URL = "https://spapi.zee5.com/singlePlayback/v2/getDetails/secure"
        headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        data = {
        'Authorization': self.TOKEN,
        'x-access-token': self.SESSION
        }
        params = {
        'content_id': id,
        'device_id': '68a30cfb-6fb3-4738-b0f5-c772ec59d450',
        'platform_name': 'androidtv_app',
        'translation': 'en',
        'user_language': 'en,hi,ta,pa',
        'country': 'IN',
        'state': 'DL',
        'app_version': '2.50.79',
        'user_type': 'premium',
        'check_parental_control': False,
   #     'uid': '90087e8f-9eb1-4c0e-a6ef-0686279409f2',
  #      'ppid': 'iuGMwSMz0HdoCQ3jrLP1000000000000',
        'version': 12
        }
        resp = self.session.post(PLAYBACK_URL, headers=headers, params=params, json=data, proxies=self.proxies).json()
        open("movie.json","w").write(json.dumps(resp))
        title = resp['assetDetails']['title']
        year = resp['assetDetails'].get('release_date', None)
        if year:
            title += f" ({year.split('-',1)[0].strip()})"
        try:
            mpdUrl = resp['assetDetails']['video_url']['mpd']
            print(resp['assetDetails']['video_url'])
        except:
            open("movie.json","w").write(json.dumps(resp))
            mpdUrl = resp['keyOsDetails']['hls_token']
        try:
           drmdata = resp['keyOsDetails']['sdrm']
        except:
            drmdata = ""
        try:
           nl = resp['keyOsDetails']['nl']
        except:
            nl = ""
        if self.xcodec == "4k":
            mpdUrl = mpdUrl.replace("manifest.mpd","manifest-connected-4k.mpd")
        return mpdUrl, title, drmdata, nl

    async def parse_m3u8(self, m3u8):
        """It will extract all the data from link"""
        try:
            yt_data = ytdl.YoutubeDL(
                                     {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True, 'proxy' : 'http://45.117.29.13:58080'}).extract_info(
                                     m3u8,
                                     download=False)
            formats = yt_data.get('formats', None)
            data = {}
            data["videos"] = []
            data["audios"] = []
            data["pssh"] = ''
            data["subtitles"] = []
            if formats:
                for i in formats:
                    format_id = i.get('format_id', '')
                    is_video = i.get("video_ext", "none") != "none"
                    is_audio = i.get("audio_ext", "none") != "none"
                    if is_audio:
                        data["audios"].append({"lang": i.get("language", "default") + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
                    if is_video:
                        data["videos"].append({"height": str(i.get("height", "default")) + f' ({bandwith_convert(int(i.get("tbr", 56) if i.get("tbr") != None else 128) * 1024)})', "id": format_id})
            else:
                raise Exception("Error in getting data")
            return data
        except Exception as e:
          #  print("error")
            raise Exception(e)
            
    async def parsempd(self, MpdUrl, retried=False):
        audioslist = []
        videoslist = []
       # print(MpdUrl)
        subtitlelist = []
        pssh = ""
        if '.m3u8' in MpdUrl:
            return await self.parse_m3u8(MpdUrl)
        mpd = self.session.get(MpdUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}, proxies=self.proxies).text
        if mpd:
            mpd = re.sub(r"<!--  -->","",mpd)
            mpd = re.sub(r"<!-- Created+(..*)","",mpd)		
            mpd = re.sub(r"<!-- Generated+(..*)","",mpd)
        try:
            mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
        except:
            if not retried and "Access Denied" in mpd:
                MpdUrl = MpdUrl.replace("manifest-connected-4k.mpd", "manifest-connected.mpd")
                return await self.parsempd(MpdUrl, True)
            self.log.error(mpd)
            raise Exception("Error")
        AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
        baseurl = MpdUrl.rsplit('manifest')[0]
        for ad in AdaptationSet:
            if pssh != "":
                break
            if ad['@mimeType'] == "audio/mp4" or ad['@mimeType'] == "video/mp4":
                if ad.get('ContentProtection') is not None:
                    for y in ad.get('ContentProtection'):
                        if y.get('@schemeIdUri') == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh = y.get('cenc:pssh')
                            break
        for ad in AdaptationSet:
            if ad['@mimeType'] == "audio/mp4":
                try:
                    auddict = {
                    'id': ad['Representation']['@id'],
                    'codec': ad['Representation'].get('@codecs', 'mp4a'),
                    'bandwidth': ad['Representation']['@bandwidth'],
                    'lang': ad['@lang'] + " " + f"({fix_codec_name(ad['Representation'].get('@codecs', 'mp4a'))} - {bandwith_convert(ad['Representation']['@bandwidth'])})"
                    }
                    audioslist.append(auddict)
                except Exception:
                    for item in ad['Representation']:
                        auddict = {
                        'id': item['@id'],
                        'codec': item['@codecs'],
                        'bandwidth': item['@bandwidth'],
                        'lang': ad['@lang'] + " " + f"({fix_codec_name(item['@codecs'])} - {bandwith_convert(item['@bandwidth'])})"
                        }
                        audioslist.append(auddict)

            if ad['@mimeType'] == "video/mp4":
                for item in ad['Representation']:
                    viddict = {
                    'width': item['@width'],
                    'height': item['@height'] + f" - {bandwith_convert(item['@bandwidth'])}",
                    'id': item['@id'],
                    'codec': item['@codecs'],
                    'bandwidth': item['@bandwidth']
                    }
                    videoslist.append(viddict)

            if ad['@mimeType'] == "text/vtt":
                subdict = {
                'id': ad['Representation']['@id'],
                'lang': ad['@lang'],
                'bandwidth': ad['Representation']['@bandwidth'],
                'url': baseurl + ad['Representation']['BaseURL']
                }
                subtitlelist.append(subdict)

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']))
        all_data = {"videos": videoslist, "audios": audioslist, "subtitles": subtitlelist, "pssh": pssh}
        return all_data
    
    async def get_input_data(self):
        """Return:
           title: str
        """
        seriesname = None
        if self.SEASON:
            seriesname, self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[self.from_ep-1].get('id'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)
        mpdUrl, title, drmdata, nl = tempData
        self.MpdDATA = await self.parsempd(mpdUrl)
    #    print(mpdUrl)
        #self.audios = await self.get_audios_ids()
        #self.videos = await self.get_videos_ids()
        return title if seriesname is None else title

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos
    
    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            episodes = []
            seriesname, IDs = self.getseries(self.mainUrl)
            for eps in IDs:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')}) 
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            for x in sorted(episodes, key=lambda k: int(k["number"])):
                try:
                    url, title, drmdata, nl = self.single(str(x['id']))
                    series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                    spisode_number = series_name.rsplit(" ",1)[1]
                    OUTPUT = os.path.join(self.filedir, seriesname)
                    MpdDATA = await self.parsempd(url)
                    is_drm = False
                    if drmdata != "":
                       pssh = self.MpdDATA["pssh"]
                       if pssh != "":
                          keys = self.do_decrypt(MpdDATA["pssh"], drmdata, nl)
                          is_drm = True
                    downloader = Downloader(url, OUTPUT)
                    await downloader.set_key(keys)
                    await downloader.set_data(MpdDATA)
                    await self.edit(f"`[+]` **Downloading Episode:** `{spisode_number}-{title}`")
                    await downloader.download(video, audios)
                    await self.edit(f"`[+]` **Decrypting Episode:** `{spisode_number}-{title}`")
                    if is_drm:
                        await downloader.set_key(keys)
                        await downloader.decrypt()
                    else:
                        await downloader.no_decrypt()   
                    await self.edit(f"`[+]` **Muxing Episode:** `{spisode_number}-{title}`")
                    await downloader.merge(series_name, self.id)
                except Exception as e:
                    print(e)
                    continue 
        else:
            try:
                self.COUNT_VIDEOS = 1
                url, title, drmdata, nl = self.SINGLE
                is_drm = False
                if drmdata != "":
                    pssh = self.MpdDATA["pssh"]
                    if pssh != "":
                        keys = self.do_decrypt(self.MpdDATA["pssh"], drmdata, nl)           
                        is_drm = True
                OUTPUT = os.path.join(self.filedir, title)
                downloader = Downloader(url, OUTPUT)
                await downloader.set_data(self.MpdDATA)
                await self.edit(f"`[+]` **Downloading:** `{title}`")
                await downloader.download(video, audios)
                await self.edit(f"`[+]` **Decrypting:** `{title}`")
                print(is_drm)
                if is_drm:
                    await downloader.set_key(keys)
                    await downloader.decrypt()
                else:
                    await downloader.no_decrypt()
                await self.edit(f"`[+]` **Muxing:** `{title}`")
                await downloader.merge(title, self.id)
            except Exception as e:
                print(e)
                
    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            pass

class Downloader:
    def __init__(self, mpdUrl, out_path, useragent="", codec="", method="", fast_dl=False, extra_audio=""):
        """url: mpd/m3u8 link
        key: kid key of drm video"""
        self.__url = mpdUrl
        self.extra_audio = extra_audio
        print(mpdUrl)
        self.__key = None
        self.fast_dl = fast_dl
        self.codec = codec
        self.old = method
        self.proxy_1 = proxy_1
        self.proxy_ = proxy_1
        # self.meg = msg
        self.opts = {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True}
        self.startTime = str(time.time())
        self.VIDEO_SUFFIXES = ("M4V", "MP4", "MOV", "FLV", "WMV", "3GP", "MPG", "WEBM", "MKV", "AVI")
        self.video_file = ""
        self.quality = "480p"
        self.selected_audios = []
        self.log = logging.getLogger(__name__)
        self.downloaded_audios = []
        self.all_data = {}
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.out_path = out_path
        if useragent=="":
            self.useragent = "KAIOS"
        else:
            self.useragent = useragent
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path, exist_ok=True)
        self.TempPath = os.path.join(self.out_path, f"temp.{time.time()}")
        if not os.path.isdir(self.TempPath):
            os.makedirs(self.TempPath)
        self.session = None
        self.downloaded_subs = []

    async def set_key(self, key):
        self.__key = key
    
    async def set_data(self, data):
        self.all_data = data

    def fix_id_ytdl(self,ytid):
        return wrap_unwrap_id(ytid.replace("/", "_"), wrap=False)
    
    def dl_subs(self):
        """Download subtitles"""
        if len(self.all_data["subtitles"]) != 0:
            self.log.info("Downloading subtitles")
        for sub in self.all_data["subtitles"]:
            if self.session is None:
                self.session = cloudscraper.create_scraper()
            if sub['lang'] == "eng" or sub['lang'] == "en" or sub['lang'] == "English":
               proxies = {
                'https': proxy
               }
               self.session.proxies.update(proxies)
               sub_file = os.path.join(os.getcwd(), self.TempPath, f'{sub["lang"]}.srt')
               sub_url = sub["url"]
               if "vod-aha.akamaized" in sub_url:
                  sub_url = sub_url.replace("_cenc_dash.ism/index.mpdtextstream_eng=1000.webvtt", "_hls.ism/textstream_eng=1000.webvtt")
               try:
                  content = self.session.get(sub_url).content
               except Exception as e:
                  self.log.error(e, exc_info=True)
                  continue
               open(sub_file, "wb").write(content)
               if os.path.exists(sub_file):
                  self.downloaded_subs.append(sub_file)
    
    async def download_url(self, quality, audio_list, custom_header=[]):
        """Download video and all audio streams using direct url""" 
        if self.all_data:
            try:
                x = None
                for x in self.all_data["videos"]:
                    if x["height"] == quality:
                        x = x["url"]
                        break
                    x = None
                if x == None:
                    for x in self.all_data["videos"]:
                        if x["height"].lower().startswith(quality.split(" ", 1)[0].lower()):
                            x = x["url"]
                            break
                        x = None
                if x == None:
                    qualities = []
                    for x in self.all_data["videos"]:
                        try:
                            qualities.append(int(x["height"].split(" ", 1)[0].strip("p")))
                        except:
                            pass
                    try:
                        quality = int(quality.split(" ", 1)[0])
                    except:
                        quality = 480
                    quality = find_nearest_quality(qualities, quality)
                    quality = str(quality)
                    for x in self.all_data["videos"]:
                        if x["height"].lower().startswith(quality):
                            x = x["url"]
                            break
                        x = None
                if x == None:
                    raise Exception("Quality not found")
                self.quality = quality
                self.selected_audios = audio_list
                self.video_file = os.path.join(os.getcwd(), self.TempPath, "_jv_drm_video" + '.mp4').replace(" ", ".")
                video_download_cmd = ["yt-dlp", "--add-header", "range:bytes=0-", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--allow-unplayable-formats", "--no-warnings", "--external-downloader", "aria2c", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o", self.video_file, x]
                print(video_download_cmd)
                if custom_header == []:
                    video_download_cmd.insert(-3, "--user-agent")
                    video_download_cmd.insert(-3, self.useragent)
                else:
                    for jv in custom_header:
                        video_download_cmd.insert(-3, "--add-header")
                        video_download_cmd.insert(-3, str(jv))
                #if "jio" in self.__url or "voot" in self.__url:
                #    video_download_cmd.insert(-3, "--proxy")
                #    video_download_cmd.insert(-3, self.proxy_)
                logging.info(video_download_cmd)
                if self.fast_dl:
                    all_dl_tasks = []
                    all_dl_tasks.append(downloadaudiocli(video_download_cmd))
                else:
                    await downloadaudiocli(video_download_cmd)
                if audio_list:
                    for audi in audio_list:
                        try:
                            my_audio = os.path.join(os.getcwd(), self.TempPath, audi.replace("(","_").replace(")","_") + '_drm.m4a').replace(" ", ".")
                            audio_format = None
                            for audio_format in self.all_data["audios"]:
                                if audio_format["lang"] == audi:
                                    audio_format = audio_format["url"]
                                    break
                            if audio_format == None:
                                for audio_format in self.all_data["audios"]:
                                    if audio_format["lang"].lower().startswith(audi.split(" ", 1)[0].lower()):
                                        audio_format = audio_format["url"]
                                        break
                                    audio_format = None
                            if audio_format == None:
                                continue
                            audio_download_cmd = ["yt-dlp", "--add-header", "range:bytes=0-", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--allow-unplayable-formats", "--no-warnings", "--external-downloader", "aria2c", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o", my_audio, audio_format]
                            if custom_header == []:
                                audio_download_cmd.insert(-3, "--user-agent")
                                audio_download_cmd.insert(-3, self.useragent)
                            else:
                                for jv in custom_header:
                                    audio_download_cmd.insert(-3, "--add-header")
                                    audio_download_cmd.insert(-3, str(jv))
                            print(audio_download_cmd)
                            if self.fast_dl:
                                all_dl_tasks.append(downloadaudiocli(audio_download_cmd))
                            else:
                                await downloadaudiocli(audio_download_cmd)
                            self.downloaded_audios.append(os.path.basename(my_audio))
                        except Exception as e:
                            self.log.exception(e)
                            continue
                #if "subtitles" in self.all_data:
                #    for sub in self.all_data["subtitles"]:
                #        my_sub = os.path.join(os.getcwd(), self.TempPath, sub["lang"] + '.vtt')
                #        sub_download_cmd = ["yt-dlp", "--allow-unplayable-formats", "--write-sub", "--sub-lang", sub["lang"], "--skip-download", self.__url,  "--geo-bypass-country", "IN", "-o", my_sub]
                #        await downloadaudiocli(sub_download_cmd) # Download subtitles
                #        os.rename(os.path.join(self.TempPath, f'{sub["lang"]}.vtt' + f'.{sub["lang"]}.vtt'), my_sub)
                print(self.downloaded_audios)
                self.dl_subs()
                if self.fast_dl:
                    await asyncio.wait_for(asyncio.gather(*all_dl_tasks), 480000)
                return 0
            except Exception as e:
                self.log.exception(e)
                return 1

    
    async def download(self, quality, audio_list, custom_header=[]):
        """Download video with format id and download all audio streams"""
        if self.all_data:
            #open("a.txt","w").write(json.dumps(audio_list))
            #open("a.json","w").write(json.dumps(self.all_data["audios"]))
            try:
                x = None
                for x in self.all_data["videos"]:
                    if "url" in x:
                        return await self.download_url(quality, audio_list, "")
                    if x["height"] == quality:
                        x = x["id"]
                        break
                    x = None
                if x == None:
                    for x in self.all_data["videos"]:
                        if x["height"].lower().startswith(quality.split(" ", 1)[0].lower()):
                            x = x["id"]
                            break
                        x = None
                if x == None:
                    qualities = []
                    for x in self.all_data["videos"]:
                        try:
                            qualities.append(int(x["height"].split(" ", 1)[0].strip("p")))
                        except:
                            pass
                    try:
                        quality = int(quality.split(" ", 1)[0])
                    except:
                        quality = 480
                    quality = find_nearest_quality(qualities, quality)
                    quality = str(quality)
                    for x in self.all_data["videos"]:
                        if x["height"].lower().startswith(quality):
                            x = x["id"]
                            break
                        x = None
                if x == None or isinstance(x, dict):
                    raise Exception("Quality not found")
                self.quality = quality.split(" ", 1)[0]
                self.selected_audios = audio_list
                self.video_file = os.path.join(os.getcwd(), self.TempPath, "_jv_drm_video" + '.mp4').replace(" ", ".")
                video_download_cmd = ["yt-dlp", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--user-agent", self.useragent, "--allow-unplayable-formats", "--format", self.fix_id_ytdl(str(x)), self.__url, "--external-downloader", "aria2c", "--no-warnings", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o",  self.video_file] 
                if custom_header != []:
                   for jv in custom_header:
                        video_download_cmd.insert(-2, "--add-header")
                        video_download_cmd.insert(-2, str(jv))
                if "jio" in self.__url or "jiocinema" in self.__url or "voot" in self.__url or "lionsgateplay" in self.__url:
                    video_download_cmd.insert(-2, "--proxy")
                    video_download_cmd.insert(-2, self.proxy_)                
                if "V2PRIME" in self.__url or "v2prime" in self.__url or "prime" in self.__url:
                    video_download_cmd.insert(-2, "--proxy")
                    video_download_cmd.insert(-2, self.proxy_)
                if "atrangii" in self.__url or "ullu" in self.__url:
                    video_download_cmd.remove("aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2")
                    video_download_cmd.remove("--downloader-args")
                    video_download_cmd.remove("--external-downloader")
                    video_download_cmd.remove("aria2c")
                print(video_download_cmd)
                if self.fast_dl:
                    all_dl_tasks = []
                    all_dl_tasks.append(downloadaudiocli(video_download_cmd))
                else:
                    e_res, t_res = await downloadaudiocli(video_download_cmd)
                    if "aria2c exited with code -1" in e_res+t_res or "ERROR:" in e_res+t_res:
                          video_download_cmd = ["yt-dlp", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--add-header", "x-playback-session-id:81b70ff3-c98c-400a-ac6e-83f0c2ce56c8", "--proxy", self.proxy_, "--user-agent", self.useragent, "--allow-unplayable-formats", "--format", self.fix_id_ytdl(str(x)), self.__url, "--external-downloader", "aria2c", "--no-warnings", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o",  self.video_file]        
                          if "V2PRIME" in self.__url or "v2prime" in self.__url or "prime" in self.__url:
                              video_download_cmd.remove("aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2")
                              video_download_cmd.remove("--downloader-args")
                              video_download_cmd.remove("--external-downloader")
                              video_download_cmd.remove("aria2c")
                          print(video_download_cmd)
                          await downloadaudiocli(video_download_cmd)
                if audio_list:
                    for audi in audio_list:
                        try:
                            my_audio = os.path.join(os.getcwd(), self.TempPath, audi + '_drm.m4a').replace(" ", ".")
                            audio_format = None
                            for audio_format in self.all_data["audios"]:  
                                if audio_format["lang"] == audi:
                                    audio_format = audio_format["id"]
                                    break
                                audio_format = None
                            #if exact audio not found then proccess with same lang but different codec
                            if audio_format == None:
                                for audio_format in self.all_data["audios"]:
                                    if audio_format["lang"].lower().startswith(audi.split(" ", 1)[0].lower()):
                                        audio_format = audio_format["id"]
                                        break
                                audio_format = None
                                
                            if audio_format == None:
                                for audio_format in self.all_data["audios"]:
                                    lang = audi.split(" ", 1)[0].lower()
                                    bit = re.search(r'\b(\d+)kbps\b', audi)
                                    bit_v = bit.group(1)
                                    band = audio_format["bandwidth"]
                                    logging.info(bit_v)
                                    logging.info(band)
                                    id = await self.find_nearest_hi_entry(self.all_data["audios"], lang, bit_v, band)
                                    audio_format = id
                                    logging.info(audio_format)           
                                    
                            if isinstance(audio_format, dict) or audio_format == None:
                                continue
                            audio_download_cmd = ["yt-dlp", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--user-agent", self.useragent, "--allow-unplayable-formats", "--format", self.fix_id_ytdl(audio_format), self.__url, "--no-warnings", "--external-downloader", "aria2c", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o", my_audio]
                            if custom_header != []:
                                for jv in custom_header:
                                    audio_download_cmd.insert(-2, "--add-header")
                                    audio_download_cmd.insert(-2, str(jv))
                            if "jiocinema" in self.__url or "jio" in self.__url or "voot" in self.__url:
                                audio_download_cmd.insert(-2, "--proxy")
                                audio_download_cmd.insert(-2, self.proxy_)
                            if "V2PRIME" in self.__url or "v2prime" in self.__url or "prime" in self.__url:
                                audio_download_cmd.insert(-2, "--proxy")
                                audio_download_cmd.insert(-2, self.proxy_)
                            if "sonyliv" in self.__url or "sonynondrmvod" in self.__url or "sony" in self.__url or "lionsgateplay" in self.__url: 
                                audio_download_cmd.insert(-2, "--proxy")
                                audio_download_cmd.insert(-2, self.proxy_)
                            print(audio_download_cmd)
                            if self.fast_dl:
                                all_dl_tasks.append(downloadaudiocli(audio_download_cmd))
                            else:
                                e_res, t_res = await downloadaudiocli(audio_download_cmd)
                                if "aria2c exited with code -1" in e_res+t_res or "ERROR:" in e_res+t_res:
                                    video_download_cmd = ["yt-dlp", "--file-access-retries", "10", "--fragment-retries", "20", "--concurrent-fragments", "5", "--add-header", "x-playback-session-id:81b70ff3-c98c-400a-ac6e-83f0c2ce56c8", "--proxy", self.proxy_, "--user-agent", self.useragent, "--allow-unplayable-formats", "--format", self.fix_id_ytdl(str(x)), self.__url, "--external-downloader", "aria2c", "--no-warnings", "--downloader-args", "aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2", "-o",  self.video_file]        
                                    if "V2PRIME" in self.__url or "v2prime" in self.__url or "prime" in self.__url:
                                        video_download_cmd.remove("aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2")
                                        video_download_cmd.remove("--downloader-args")
                                        video_download_cmd.remove("--external-downloader")
                                        video_download_cmd.remove("aria2c")
                                    print(video_download_cmd)
                                    await downloadaudiocli(video_download_cmd)
                            if "429: Too Many Requests" in e_res+t_res or "Too Many Requests" in e_res+t_res:
                               print("Audio Downloading Failed Skipping it")
                               continue 
                            else:
                               self.downloaded_audios.append(os.path.basename(my_audio))
                        except Exception as e:
                            self.log.exception(e)
                            continue
            #    if "subtitles" in self.all_data: 
                   # for sub in self.all_data["subtitles"]:
                       ## my_sub = os.path.join(os.getcwd(), self.TempPath, sub["lang"] + '.vtt')
                     #   sub_download_cmd = ["yt-dlp", "--allow-unplayable-formats", "--write-sub", "--sub-lang", sub["lang"], "--skip-download", self.__url,  "--geo-bypass-country", "IN", "-o", my_sub]
                   #     print(sub_download_cmd)
                       ## c = await downloadaudiocli(sub_download_cmd)
                    #    print(c)# Download subtitles
                    #    os.rename(os.path.join(self.TempPath, f'{sub["lang"]}.vtt' + f'.{sub["lang"]}.vtt'), my_sub)
                self.dl_subs()
                if self.fast_dl:
                    await asyncio.wait_for(asyncio.gather(*all_dl_tasks), 480000)
                return 0
            except Exception as e:
                self.log.exception(e)
                return 1
   
    async def find_nearest_hi_entry(self, data, bit, target_bandwidth, band):
        hi_entries = []
        for entry in data:
            if bit in entry['lang'].lower():
                hi_entries.append(entry)
        self.log.info(hi_entries)
        if hi_entries:
            nearest_entry = min(hi_entries, key=lambda x: abs(int(band)) - int(target_bandwidth))
            if nearest_entry:
                return nearest_entry['id']
        return data[-1]['id']

    async def decrypt(self, ty=""):
        """Decrypt all downloaded streams"""
        if ty == "HOICHOI":
            all_files = self.downloaded_audios 
        elif ty == "NF":
           all_files = [os.path.basename(self.video_file)]
           self.nf_audios = []
           for file in self.downloaded_audios:
               newpath = os.path.join(os.getcwd(), self.TempPath, file).replace(" ", ".")
               self.nf_audios.append(newpath)
        else:
            all_files = self.downloaded_audios + [os.path.basename(self.video_file)]
        temp_audios = []
        try:
            for my_file in all_files:
                old_path = os.path.join(os.getcwd(), self.TempPath, my_file)
                old_path = old_path.replace(" ", ".")
                new_path = os.path.join(os.getcwd(), self.TempPath, my_file.replace(" ", "_").rsplit("_", 1)[0].rsplit(".", 1)[0].replace(".", "_") + "_jv.mp4")
                new_path = new_path.replace(" ", ".")
                if ty == "HOICHOI":
                    temp_audios.append(new_path)
                else:
                   if old_path.upper().endswith(self.VIDEO_SUFFIXES):
                      self.video_file = new_path
                   else:
                      temp_audios.append(new_path)
                if ty == "AHA" or ty == "AMZN" or ty == "SXT" or ty == "NF":
                   cmd = "wine mp4decrypt.exe"
                else:
                   cmd = "mp4decrypt"
                for key in self.__key:
                    cmd += f" --key {str(key)}"
                cmd += f''' "{old_path}" "{new_path}"'''
                print(cmd)
                st, stout = await run_comman_d(cmd)
                self.log.info(st + stout)
                os.remove(old_path)
        except Exception as e:
            self.log.exception(e)
      #      continue
        self.downloaded_audios = temp_audios
        
    async def no_decrypt(self, ty=""):
        """set all non-drm downloaded streams"""
        all_files = self.downloaded_audios + [os.path.basename(self.video_file)]
        temp_audios = []
        for my_file in all_files:
            old_path = os.path.join(os.getcwd(), self.TempPath, my_file)
            old_path = old_path.replace(" ", ".")
            new_path = os.path.join(os.getcwd(), self.TempPath, my_file.replace(" ", "_").rsplit("_", 1)[0].rsplit(".", 1)[0].replace(".", "_") + "_jv.mp4")
            new_path = new_path.replace(" ", ".")
            if old_path.upper().endswith(self.VIDEO_SUFFIXES):
                self.video_file = new_path
            else:
                temp_audios.append(new_path)
            cmd = "mp4decrypt"
            os.rename(old_path, new_path)
        self.downloaded_audios = temp_audios
    
    async def get_info(self, file):
        mediainfo_output = subprocess.Popen(
            ["mediainfo", "--Output=JSON", "-f", file],
            stdout=subprocess.PIPE,
        )
        return json.load(mediainfo_output.stdout)

    async def get_videoinfo(self, path):
        video_file = path
        data = await self.get_info(video_file)
        video_track = [x for x in data["media"]["track"] if x["@type"] == "Video"]
        if video_track == []:
            video_track = video_track[0]
        cdec = video_track[0]["Format"].lower()
        if "avc" in cdec:
            v_codec = "x264"
        elif "hev" in cdec or "hvc" in cdec:
            v_codec = "x265" 
        elif "vp9" in cdec or "v_vp9" in cdec:
            v_codec = "VP9"
        return v_codec
        
    async def get_audioinfo(self, files):
        try:
           audio = files[0]
        except:
            audio = self.video_file
        data = await self.get_info(audio)
        audio_track = [x for x in data["media"]["track"] if x["@type"] == "Audio"]
        audio_track = audio_track[0]
#        print(audio_track)
        try:
           if int(audio_track["Channels"]) == 8:
              ch = "7.1"
           elif int(audio_track["Channels"]) == 6:
              ch = "5.1"
           elif int(audio_track["Channels"]) == 2:
              ch = "2.0"
           elif int(audio_track["Channels"]) == 1:
              ch = "1.0"
           else:
              ch = "5.1"
        except:
            ch = ""
        if audio_track["Format"] == "E-AC-3":
            codec = "DD+"
        elif audio_track["Format"] == "AC-3":
            codec = "DD"
        elif audio_track["Format"] == "AAC":
            codec = "AAC"
        elif audio_track["Format"] == "DTS":
            codec = "DTS"
        elif "DTS" in audio_track["Format"]:
            codec = "DTS"
        else:
            codec = "DD+"
       # brte = audio_track['Bit rate']
        return codec, ch
        
    async def get_bitrate(self):
        try:
           match = re.search(r'\((.*?)\)', self.selected_audios[0])
           if match:
              ad = match.group(0)
              ad = ad.split(" - ")[-1]
           X = {"135)" : "128)", "197kbps)" : "192Kbps)", "135kbps)" : "128Kbps)", "71kbps)" : "64Kbps)", "257kbps)" : "256Kbps)", "193kbps)" : "192Kbps)", "130kbps)" : "128Kbps)", "139kbps)" : "128Kbps)", "74kbps)" : "64Kbps)", "129kbps)" : "128Kbps)", "65kbps)" : "64Kbps)", "72kbps)" : "64Kbps)", "125kbps)" : "128Kbps"}
           bitrate = X.get(str(ad), str(ad)).replace(")", "")
        except:
            bitrate = ""
        return bitrate
        
    async def get_mediainfo(self):
        video_file = self.video_file
        try:
          audios = self.nf_audios
        except:
           audios = self.downloaded_audios
        v_codec = await self.get_videoinfo(video_file)
        audio_format, channel = await self.get_audioinfo(audios)
        bitrate = await self.get_bitrate()
        return v_codec, audio_format, channel, bitrate
    
    async def get_audselection(self):
        audios = self.selected_audios
        list = []
        for i in audios:
            aud = i.split(" ")[0]
            list.append(aud)
        final_list = [LANGUAGE_SHORT_FORM.get(x, x) for x in list]
        return final_list
        
    async def merge(self, output_filename, meg, type_="ZEE5"):
        """Merge all downloaded stream"""
        mf = await db.get_user(meg) 
        if mf["mkv"] == "mkv":
            outfor = "mkv"
        else:
            outfor = "mp4"
        if type_ == "NF":
          audios = self.nf_audios
        else:
           audios = self.downloaded_audios
     
        audios_names = await self.get_audselection()
        all_files = self.downloaded_subs + [self.video_file] + audios 
        v_codec, audio_format, channel, bitrate = await self.get_mediainfo()
        subtitles = self.downloaded_subs
        self.quality = self.quality.split(" ", 1)[0]
        if len(self.downloaded_subs) > 0:
           subs = self.downloaded_subs[0]
        else:
           subs = ""
        if mf["format"] == "f":
            if len(self.selected_audios) == 1:
                file_name = f"{output_filename} {self.quality}p {type_} WEB-DL {v_codec} [{' + '.join(LANGUAGE_FULL_FORM.get(x.lower(), x.capitalize()) for x in audios_names)} ({audio_format} {channel} - {bitrate})] _Esub_{Config.TAG}.{outfor}"
            else:
                file_name = f"{output_filename} {self.quality}p {type_} WEB-DL {v_codec} ({audio_format} {channel} - {bitrate}) [{' + '.join(LANGUAGE_SHORT_FORM.get(x.lower(), x.capitalize()) for x in audios_names)}] _Esub_{Config.TAG}.{outfor}"
        else:
           if type_ == "Shemaroome":
               file_name = f"{output_filename} {self.quality}p {type_} WEB-DL {self.extra_audio} {audio_format} {channel} {v_codec}-{Config.TAG}.{outfor}".replace(" ", ".").replace("(", "").replace(")", "").replace("..", ".")
           elif len(self.selected_audios) == 1:
                  file_name = f"{output_filename} {self.quality}p {type_} WEB-DL {' + '.join(LANGUAGE_FULL_FORM.get(x.lower(), x.capitalize()) for x in audios_names)} {audio_format} {channel} {v_codec}-{Config.TAG}.{outfor}".replace(" ", ".").replace("(", "").replace(")", "").replace("..", ".") 
           elif len(self.selected_audios) == 2:
                  file_name = f"{output_filename} {self.quality}p {type_} WEB-DL DUAL {audio_format} {channel} {v_codec}-{Config.TAG}.{outfor}".replace(" ", ".").replace("(", "").replace(")", "").replace("..", ".")
           elif len(self.selected_audios) > 2:
                 file_name = f"{output_filename} {self.quality}p {type_} WEB-DL MULTi {audio_format} {channel} {v_codec}-{Config.TAG}.{outfor}".replace(" ", ".").replace("(", "").replace(")", "").replace("..", ".")
           else:
                 file_name = f"{output_filename} {self.quality}p {type_} WEB-DL {audio_format} {channel} {v_codec}-{Config.TAG}.{outfor}".replace(" ", ".").replace("(", "").replace(")", "").replace("..", ".")
        file_name = os.path.join(self.out_path, file_name)
        if type_ == "HOICHOI" or outfor == "mp4":
           cmd = f'mkvmerge -o "{file_name}"'
           for file in audios:
               cmd+= f' --track-name 0:"ANToNi - [{audio_format} {channel} - {bitrate}]" "{file}" '
           for file in self.downloaded_subs:
               cmd+= f'--language 0:eng --track-name 0:"ANToNi - Subtitles" "{file}" '
           cmd+= f' "{self.video_file}" '
           st, stout = await run_comman_d(cmd)     
        else:
           cmd = f'ffmpeg -y -i "{self.video_file}" '
           audios = audios
           for audio in audios:
               cmd += f'-i "{audio}" '
           if os.path.exists(subs):
              cmd+= f' -i "{self.downloaded_subs[0]}" '
           if len(self.downloaded_audios) == 0:
              cmd += "-map 0 "
           else:
              cmd +="-map 0:v "
           for i in range(1, len(audios)+1):
              cmd+=f"-map {i}:a? "
           if os.path.exists(subs):
              stream = len(audios)+1
              cmd+= f'-map {stream}:s -metadata:s:s:0 language=eng -metadata:s:s:0 title="ANToNi.English." '
           step = 0
           for audio in audios:
               cmd += f'-metadata:s:a:{step} title="ANToNi - [{audio_format} {channel} - {bitrate}]" '
               step += 1
           cmd += f'-c:v copy -c:a copy "{file_name}"'
           st, stout = await run_comman_d(cmd)
        
        os.remove(self.video_file)
        await asyncio.sleep(3)
        for aud_file in all_files:
            try:
                os.remove(aud_file)
            except Exception as e:
                continue                
        try:
            os.remove(self.video_file)
        except:
            pass 
        for sub in self.downloaded_subs:
            try: 
                os.remove(sub)
            except:
                continue 
        try:
            shutil.rmtree(self.TempPath)
        except:
            pass

        try:
          for item in os.listdir(self.out_path):
              item_path = os.path.join(self.out_path, item)
              if os.path.isdir(item_path):
                 shutil.rmtree(item_path)
        except Exception as e:
          pass
         
        return file_name
