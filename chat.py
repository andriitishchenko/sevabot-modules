#!/sevabot
# -*- coding: utf-8 -*-

#http://skype4py.sourceforge.net/doc/html/Skype4Py.utils-pysrc.html#CachedCollection.Item

from __future__ import unicode_literals

import sys
# sys.path.append('~/sevabot/libs/pygoogle.py')

import os
import re
import logging
# import requests
from bs4 import BeautifulSoup
import urllib2
import logging
import datetime
import random
from time import gmtime, strftime
# import html2text
# from pygoogle import pygoogle
import pickle
from collections import OrderedDict

from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id
import Skype4Py


BOT_NAME = "alex"

logger = logging.getLogger("TessChat")
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)
logger.debug("Tess Chat module level load import")

class TessChat(StatefulSkypeHandler):
    """
    Print help text to chat.
    """
    
    def init(self, sevabot):
        """
        Print help text to chat.
        """
        self.skype = sevabot.getSkype()
        self.sevabot = sevabot
        self.commands = {
            "деплой": self.cmd_deploy,
            "время": self.cmd_time,
            "загугли": self.cmd_search,
            "(привет|hi|здаров)": self.cmd_hi,
            "что такое": self.cmd_what_is,
            "стреляй": self.cmd_shut,
            "(man|help)": self.cmd_man,
        }
        self.publickcommands = {
            "(привет|hi|здаров)": self.cmd_hi,
        }

    def handle_message(self, msg, status):
        """
        Print help text to chat.
        """
        if status == 'SENT':
           return True

        body = ensure_unicode(msg.Body)
        lower = body.lower()
        words = re.split('(\s+|\n|,)', lower, flags=re.M)

        if len(words) < 2:
            return False

        if False==words[0].startswith(BOT_NAME):
            return False            

        chat_id = get_chat_id(msg.Chat)

        # usrs = msg.Chat.Members
        # aUm = iter(usrs)
        # for i, x in enumerate(usrs):
        #     msg.Chat.SendMessage(" - %s" % x.FullName)

        # Check if we match any of our commands
        for name, cmd in self.commands.items():
            patern = re.compile(name)
            if patern.search(lower) != None:
                cmd(msg, chat_id)
                return True
        return False
    
    def shutdown(self):
        """
        Print help text to chat.
        """

    def register_callback(self, skype, event, callback):
        """
        Print help text to chat.
        """
        return skype.RegisterEventHandler(event, callback)

    def unregister_callback(self, skype, event, callback):
        """
        Print help text to chat.
        """
        return skype.UnregisterEventHandler(event, callback)

    # @staticmethod
    def get_link_title(e,url):
        """
        Print help text to chat.
        """
        try:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            return soup.title.string        
        except:
            return None

    def cmd_man(self, msg, chat_id):
        """
        Print help text to chat.
        """
        string = """Умею:
        !dice, 
        !ping, 
        !sad, 
        !weather,
        деплой,
        время,
        привет,
        что такое <string>?,
        стреляй,
        man"""
        msg.Chat.SendMessage(string)

    def cmd_deploy(self, msg, chat_id):
        """
        Print help text to chat.
        """
        msg.Chat.SendMessage("деплою потихоньку...")
    
    def cmd_time(self, msg, chat_id):
        """
        Print help text to chat.
        """
        msg.Chat.SendMessage("%s" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    def cmd_search(self, msg, chat_id):
        """
        Print help text to chat.
        """
        msg.Chat.SendMessage("ничего не нашел")
    
    def cmd_hi(self, msg, chat_id):
        """
        Print help text to chat.
        """        
        # self.hi_file = os.path.join(os.path.dirname(__file__), "hi.tmp")
        # self.hi_history = Hihistory.read(self.hi_file)
        msg.Chat.SendMessage("%s, привет!" % msg.FromDisplayName);

    def cmd_shut(self, msg, chat_id):
        """
        Print help text to chat.
        """        
        random.seed()
        usrs = msg.Chat.Members
        index = random.randint(0, usrs.Count-1)
        user = usrs[index]
        msg.Chat.SendMessage("%s убит! (yn) " % user.FullName)
        # aUm = iter(usrs)
        # for i, x in enumerate(usrs):
            # msg.Chat.SendMessage(" - %s" % x.FullName)

    def cmd_what_is(self, msg, chat_id):
        """
        Print help text to chat.
        """
        # search = re.compile('(?<=что такое\s).\w+')
        # search = re.compile('(?<=что такое\s)[^\s]*')
        search = re.compile('(?<=что такое\s)[^?]*')
        # 
        
        body = ensure_unicode(msg.Body)
        lower = body.lower()
        whatis_text = search.findall(lower)
        if whatis_text!=None:
            new_url = "http://ru.wikipedia.org/wiki/"+whatis_text[0].replace (" ", "_")
            msg.Chat.SendMessage("глянь тут %s" % new_url)  

            # str_wiki = self.get_wiki_text(new_url)
            # msg.Chat.SendMessage("%s" % str_wiki) 
            # if str_wiki!=None:
            #     msg.Chat.SendMessage("%s" % str_wiki) 
  

    # def get_wiki_text(e,url):
    #     """
    #     Print help text to chat.
    #     """
    #     rez = "None1"
    #     content = urllib2.urlopen(url).read()
    #     soup = BeautifulSoup(content)
    #     div = soup.find("div", {"id": "mw-content-text "})
    #     rez = div
    #     return rez

        # try:
        #     content = urllib2.urlopen(url).read()
        #     soup = BeautifulSoup(content)
        #     # div = soup.find("div", {"id": "noarticletext"})
        #     # if div!=None:
        #     #     return None
            
        #     div = soup.find("div", {"id": "mw-content-text "})
        #     # rez = div.first('p').renderContents()
        #     rez = div.renderContents()
        #     # .contents[0]
        #     # h = html2text.HTML2Text()
        #     # h.ignore_links = True
        #     # print h.handle("<p>Hello, <a href='http://earth.google.com/'>world</a>!")
        #     # return soup.title.string        
        # except:
        #     rez = "EEER"
        # return rez
# class Hihistory:
#     """
#     Stored pickled state of the tasks.

#     Use Python pickling serialization for making status info persistent.
#     """

#     def __init__(self):
#         # Chat id -> OrderedDict() of jobs mappings
#         self.records = dict()

#     @classmethod
#     def read(cls, path):
#         """
#         Read status file.

#         Return fresh status if file does not exist.
#         """

#         if not os.path.exists(path):
#             # Status file do not exist, get default status
#             return Hihistory()

#         f = open(path, "rb")

#         try:
#             return pickle.load(f)
#         finally:
#             f.close()

#     @classmethod
#     def write(cls, path, status):
#         """
#         Write status file
#         """
#         f = open(path, "wb")
#         pickle.dump(status, f)
#         f.close()

#     def get_tasks(self, chat_id):
#         """
#         Get jobs of a particular chat.
#         """
#         if not chat_id in self.records:
#             # Skype username -> Task instance mappings
#             self.records[chat_id] = OrderedDict()

#         return self.records[chat_id]

# class Rec:
#     """
#     """

#     def __init__(self, real_name, started, desc):
#         """
#         """
#         self.chat_id = started
#         self.user_id = desc
#     # The following has been
#     # ripped off from https://github.com/imtapps/django-pretty-times/blob/master/pretty_times/pretty.py
  

# Export the instance to Sevabot
sevabot_handler = TessChat()
__all__ = ['sevabot_handler']
